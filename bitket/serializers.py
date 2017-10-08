import logging
from collections import OrderedDict
from time import sleep
from decimal import Decimal
from random import random

from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from localflavor.se.forms import SEPersonalIdentityNumberField
import stripe
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_expandable import ExpandableSerializerMixin
from rest_framework_jwt.utils import jwt_payload_handler as original_jwt_payload_handler

from . import exceptions, models

logger = logging.getLogger(__name__)


def jwt_payload_handler(user):
    payload = original_jwt_payload_handler(user)
    payload['name'] = user.get_full_name()
    payload['nin'] = user.nin
    return payload


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            'url',
            'id',
            'slug',
            'name',
            'description',
            'organization'
        ]


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Organization
        fields = [
            'url',
            'id',
            'name',
            'organization_number',
            'address',
            'email'
        ]


class PurchasePaymentSerializer(serializers.Serializer):
    # Hard coded to Stripe for the time being.
    type = serializers.ChoiceField(choices=(('stripe', _('Stripe')),))
    payload = serializers.CharField()
    amount = serializers.DecimalField(max_digits=9, decimal_places=2)


class PurchaseTicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Ticket
        fields = (
            'url',
            'id',
            'ticket_type',
            'variation_choices'
        )
        extra_kwargs = {
            'ticket_type': {
                # Don't filter on general availability! We might have access
                # codes.
                'queryset': models.TicketType.objects.published()
            }
        }

    def validate(self, attrs):
        if (list(models.Variation.objects.filter(choices__in=attrs['variation_choices']).distinct()) != list(attrs['ticket_type'].variations.all()) or len(attrs['variation_choices']) != attrs['ticket_type'].variations.count()):
            raise exceptions.InvalidVariationChoices(_('Invalid variation choices.'))

        return attrs


class PurchaseTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Transaction
        fields = (
            'amount',
        )


class PurchaseMessageSerializer(serializers.Serializer):
    code = serializers.CharField()
    text = serializers.CharField()
    entity = serializers.CharField()


class PurchaseUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'nin',
        )
        extra_kwargs = {
            'nin': {'max_length': 13}  # Allow YYYYMMDD-XXXX
        }

    def validate_nin(self, value):
        return SEPersonalIdentityNumberField(required=False, coordination_number=False).clean(value=value)


class PurchaseSerializer(serializers.Serializer):
    tickets = PurchaseTicketSerializer(
        many=True,
        allow_empty=False)

    # Request only
    access_codes = serializers.SlugRelatedField(
        write_only=True,
        many=True,
        slug_field='token',
        queryset=models.AccessCode.objects.utilizable(),
        allow_empty=True)
    payment = PurchasePaymentSerializer(
        write_only=True)
    user = PurchaseUserSerializer(
        write_only=True)

    # Response only
    messages = PurchaseMessageSerializer(
        read_only=True,
        many=True,
        allow_empty=True)
    transactions = PurchaseTransactionSerializer(
        read_only=True,
        many=True,
        allow_null=True)

    def validate_tickets(self, value):
        used_ticket_type_ids = [t.get('ticket_type').id for t in value]

        # We only want exactly one organization. Many organizations *can* be
        # handled but implicates troubles if payment to one organization
        # succeeds but not to another.
        if models.Organization.objects.filter(
            events__ticket_types__id__in=used_ticket_type_ids
        ).distinct().count() != 1:
            raise exceptions.MultipleOrganizations()

        if models.TicketType.objects.filter(
            id__in=used_ticket_type_ids,
            conflicts_with__id__in=used_ticket_type_ids
        ).exists():
            raise exceptions.ConflictingTicketTypes()

        return value

    def create(self, validated_data):
        # * Validate ticket types according to general avail. and access code
        # * Create ticket objects
        # * Charge with Stripe
        # * Rollback transaction if Stripe fails

        response_data = OrderedDict((
            ('tickets', []),
            ('transactions', []),
            ('messages', [])
        ))

        request = self.context['request']
        user = request.user

        tickets_data = validated_data.get('tickets')
        # We've already validated there is only one organization in play here.
        organization = tickets_data[0]['ticket_type'].event.organization

        unclear_tickets = set()
        safe_tickets = set()
        lost_tickets = set()

        with transaction.atomic():
            for ticket_data in tickets_data:
                for access_code in validated_data.get('access_codes'):
                    if access_code and access_code.ticket_type == ticket_data['ticket_type']:
                        ticket_data['access_code'] = access_code
                # Keeping M2M until we have saved
                variation_choices = ticket_data.pop('variation_choices')
                ticket = models.Ticket.objects.create(pending=True, **ticket_data)
                ticket.variation_choices.set(variation_choices)
                models.TicketOwnership.objects.create(ticket=ticket, user=user)
                unclear_tickets.add(ticket)
        try:
            while True:
                for ticket in unclear_tickets:
                    if not ticket.ticket_type.is_generally_available:
                        # Ticket type not available for purchase
                        if not ticket.access_code:
                            lost_tickets.add(ticket)
                            response_data['messages'].append(dict(
                                code='ticket_type_unavailable',
                                text=_("The ticket type '{}' is not available for purchase.".format(
                                        ticket.ticket_type.name)),
                                entity=reverse('tickettype-detail', kwargs={
                                    'pk': ticket.ticket_type_id}, request=request)))
                            continue

                        # Access code is supplied, has an impact on availability
                        # and is utilized by a ticket before this one.
                        if ticket.access_code and ticket.access_code.tickets.before_in_queue(ticket=ticket).exists():
                            lost_tickets.add(ticket)
                            response_data['messages'].append(OrderedDict((
                                ('code', 'access_code_utilized'),
                                ('text', _("The access code is already utilized."))
                            )))
                            continue

                    if models.Ticket.objects.filter(ticket_type__conflicts_with=ticket.ticket_type).before_in_queue(ticket=ticket).owned_by(user).exists():
                        lost_tickets.add(ticket)
                        response_data['messages'].append(dict(
                            code='ticket_type_conflicting',
                            text=_('The ticket type conflicts with another ticket of yours.'),
                            entity=reverse('tickettype-detail', kwargs={'pk': ticket.ticket_type_id}, request=request)
                        ))
                        continue

                    # No tickets left
                    if not ticket.ticket_type.within_max_total_quantity:
                        lost_tickets.add(ticket)
                        response_data['messages'].append(OrderedDict((
                            ('code', 'ticket_type_max_total_quantity_exceeded'),
                            ('text', _("There are no tickets of the type '{}' left.".format(ticket.ticket_type.name))),
                            ('entity', reverse('tickettype-detail', kwargs={'pk': ticket.ticket_type_id}, request=request))
                        )))
                        continue

                    if ticket.ticket_type.max_personal_quantity and ticket.ticket_type.tickets.before_in_queue(ticket=ticket).owned_by(user).count() >= ticket.ticket_type.max_personal_quantity:
                        lost_tickets.add(ticket)
                        response_data['messages'].append(OrderedDict((
                            ('code', 'ticket_type_max_personal_quantity_exceeded'),
                            ('text', _(
                                "You have reached your personal limit for the ticket type '{}'.".format(
                                    ticket.ticket_type.name))),
                            ('entity', reverse('tickettype-detail', kwargs={
                                'pk': ticket.ticket_type_id}, request=request))
                        )))
                        continue

                    max_total_quantity = ticket.ticket_type.max_total_quantity
                    position = ticket.ticket_type.tickets.before_in_queue(ticket=ticket).count()

                    # position is zero-indexed
                    if not max_total_quantity or position < max_total_quantity:
                        # Since the position never gets higher, we now know that
                        # this ticket is safe. Great!
                        safe_tickets.add(ticket)
                        continue

                    # Everything above this position will be discarded.
                    cutoff_position = 2 * max_total_quantity - ticket.ticket_type.tickets.unpending().count()

                    # Cutting off randomly (although weighted) up to the point
                    # where there are as many pending over the maximum quantity
                    # as under it. (Beneath this point all are discarded)
                    if random() <= (
                            (position - max_total_quantity) /
                            (cutoff_position - max_total_quantity or 0.001)  # Save us from ZeroDivisionError
                            ) ** 3:  # Make it much harder near the cutoff
                        lost_tickets.add(ticket)
                        response_data['messages'].append(OrderedDict((
                            ('code', 'bad_queue_position'),
                            ('text', _(
                                "You didn't get a good enough queue position to get the ticket '{}'.".format(
                                    ticket.ticket_type.name))),
                            ('entity', reverse('tickettype-detail', kwargs={
                                'pk': ticket.ticket_type_id}, request=request))
                        )))
                        continue

                unclear_tickets = unclear_tickets.difference(safe_tickets,
                                                             lost_tickets)

                # Delete all lost tickets so we release the positions to
                # concurrent buyers
                for ticket in lost_tickets:
                    ticket.delete()
                lost_tickets.clear()

                if unclear_tickets:
                    # Wait for a while and retry.
                    sleep(0.5)
                    continue
                else:
                    # We know every ticket's destiny.
                    break

        except Exception as exc:
            # Something went really wrong and we must clean up the mess before
            # raising the exception.
            for ticket in unclear_tickets | safe_tickets | lost_tickets:
                ticket.delete()

            raise exc

        if safe_tickets:
            charge_amount = Decimal(0)

            for ticket in safe_tickets:
                # There should be one ownership per ticket, hence get()
                charge_amount += ticket.ownerships.get().price

            try:
                assert charge_amount <= validated_data['payment']['amount']

                charge = stripe.Charge.create(
                    stripe_account=organization.stripe_account_id,
                    source=validated_data['payment']['payload'],
                    amount=int(charge_amount * 100),
                    currency=settings.CURRENCY,
                    receipt_email=user.email,
                    metadata=dict(
                        bitket_ticket_ownerships=','.join(map(lambda x: str(x.ownerships.get().pk), safe_tickets))
                    )
                )
            except Exception as exc:
                # Something went wrong and we must clean up the mess.
                for ticket in safe_tickets:
                    ticket.delete()

                if isinstance(exc, stripe.error.CardError):
                    # See https://stripe.com/docs/api#errors
                    error = exc.json_body['error']
                    raise exceptions.PaymentFailed(error['message'])

                raise exc

            purchase_transaction = models.Transaction.objects.create(
                amount=charge_amount,
                stripe_charge=charge.id
            )
            response_data['transactions'].append(purchase_transaction)

            # Must be done before sending the confirmation emails
            user.nin = validated_data['user']['nin']
            user.save()

            for ticket in safe_tickets:
                ticket.pending = False
                ticket_ownership = ticket.ownerships.latest()
                purchase_transaction.ticket_ownerships.add(ticket_ownership)
                ticket.save()
                response_data['tickets'].append(ticket)
                try:
                    ticket_ownership.email_confirmation()
                except Exception as exc:
                    # This should not stop us.
                    logger.exception('Exception during mail send')

        return response_data


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Ticket
        fields = [
            'url',
            'id',
            'ticket_type',
            'variation_choices',
            'utilized'
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'url',
            'id',
            'name',
            'email'
        ]


class PrivilegedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'url',
            'id',
            'name',
            'nin',
            'email'
        ]


class TicketOwnershipSerializer(ExpandableSerializerMixin,
                                serializers.HyperlinkedModelSerializer):
    resell_token = serializers.SerializerMethodField()
    qr = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    utilized = serializers.SerializerMethodField()

    class Meta:
        model = models.TicketOwnership
        fields = [
            'url',
            'id',
            'ticket',
            'user',
            'code',
            'qr',
            'price',
            'resell_token',
            'is_current',
            'utilized'
        ]
        expandable_fields = {
            'ticket': (TicketSerializer, list(), dict()),
            'user': (PrivilegedUserSerializer, list(), dict())
        }

    def get_qr(self, obj):
        if obj.is_current:
            return b'data:image/png;base64,' + obj.get_qr()
        return None

    def get_resell_token(self, obj):
        if self.context['request'].user != obj.user:
            return None
        return obj.resell_token

    def get_utilized(self, obj):
        return obj.ticket.utilized

class VariationChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VariationChoice
        fields = [
            'url',
            'id',
            'variation',
            'name',
            'delta',
            'index'
        ]


class VariationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Variation
        fields = [
            'url',
            'id',
            'ticket_type',
            'name',
            'index'
        ]


class _VariationSerializer(VariationSerializer):
    choices = VariationChoiceSerializer(many=True)

    class Meta:
        model = models.Variation
        fields = [
            'url',
            'id',
            'name',
            'choices'
        ]


class AccessCodeSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = models.AccessCode
        fields = [
            'token',
            'ticket_type',
        ]

    def get_token(self, obj):
        return self.context['view'].kwargs.get('token', obj.token)


class TicketTypeSerializer(serializers.HyperlinkedModelSerializer):
    modifiers = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()

    class Meta:
        model = models.TicketType
        fields = [
            'url',
            'id',
            'event',
            'name',
            'description',
            'price',
            'modifiers',
            'availability',
            'conflicts_with',
            'index'
        ]

    def get_availability(self, obj):
        return OrderedDict((
            ('general', obj.is_generally_available),
            ('total_quantity', obj.within_max_total_quantity)
        ))

    def get_modifiers(self, obj):
        class _ModifierSerializer(serializers.ModelSerializer):
            condition = serializers.SerializerMethodField()

            class Meta:
                model = models.Modifier
                fields = [
                    'condition',
                    'delta'
                ]

            def get_condition(self, obj):
                return '{}'.format(obj.condition_subclass)

        user = self.context['request'].user
        modifiers = obj.modifiers.eligible(user).select_related('condition')
        serializer = _ModifierSerializer(modifiers, read_only=True, many=True)
        return serializer.data
