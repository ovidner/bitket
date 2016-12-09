import logging
from collections import OrderedDict
from time import sleep

from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from localflavor.se.forms import SEPersonalIdentityNumberField
import stripe
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework_jwt.utils import jwt_payload_handler as original_jwt_payload_handler

from tickle import exceptions, models

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
            'name'
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

    def validate_nin(self, value):
        return SEPersonalIdentityNumberField(coordination_number=False).clean(value=value)


class PurchaseSerializer(serializers.Serializer):
    tickets = PurchaseTicketSerializer(
        many=True)

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

        user = self.context['request'].user

        tickets_data = validated_data.get('tickets')
        used_ticket_type_ids = [t.get('ticket_type').id for t in tickets_data]

        # We only want exactly one organization. Many organizations *can* be
        # handled but implicates troubles if payment to one organization
        # succeeds but not to another.
        try:
            organization = models.Organization.objects.filter(
                events__ticket_types__id__in=used_ticket_type_ids
            ).distinct().get()
        except models.Organization.MultipleObjectsReturned:
            raise exceptions.MultipleOrganizations()

        if models.TicketType.objects.filter(
            id__in=used_ticket_type_ids,
            conflicts_with__id__in=used_ticket_type_ids
        ).exists():
            raise exceptions.ConflictingTicketTypes()

        with transaction.atomic(using=settings.SERIALIZABLE_ISOLATION):
            unclear_tickets = set()
            safe_tickets = set()
            lost_tickets = set()

            # Creates all ticket objects right away to ensure a reasonably fair
            # position in the queue. We'll do all necessary validations later
            # on.
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
                                    'pk': ticket.ticket_type_id})))
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
                            entity=reverse('tickettype-detail', kwargs={'pk': ticket.ticket_type_id})
                        ))
                        continue

                    # No tickets left
                    if not ticket.ticket_type.within_max_total_quantity:
                        lost_tickets.add(ticket)
                        response_data['messages'].append(OrderedDict((
                            ('code', 'ticket_type_max_total_quantity_exceeded'),
                            ('text', _("There are no tickets of the type '{}' left.".format(ticket.ticket_type.name))),
                            ('entity', reverse('tickettype-detail', kwargs={'pk': ticket.ticket_type_id}))
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
                                'pk': ticket.ticket_type_id}))
                        )))
                        continue

                    position = ticket.ticket_type.tickets.before_in_queue(ticket=ticket).count()

                    # position is zero-indexed
                    if (not ticket.ticket_type.max_total_quantity or
                            position < ticket.ticket_type.max_total_quantity):
                        # Since the position never gets higher, we now know that
                        # this ticket is safe. Great!
                        safe_tickets.add(ticket)

                unclear_tickets = unclear_tickets.difference(safe_tickets,
                                                             lost_tickets)
                if unclear_tickets:
                    # Wait for a while and retry.
                    sleep(0.1)
                    continue
                else:
                    # We know every ticket's destiny.
                    break

            # Delete all lost tickets so we release the positions to concurrent
            # buyers
            for ticket in lost_tickets:
                ticket.delete()

            if safe_tickets:
                charge_amount = Decimal(0)

                for ticket in safe_tickets:
                    # There should be one ownership per ticket, hence get()
                    charge_amount += ticket.ownerships.get().price

                assert charge_amount <= validated_data['payment']['amount']

                user.nin = validated_data['user']['nin']
                user.save()

                try:
                    charge = stripe.Charge.create(
                        stripe_account=organization.stripe_account_id,
                        source=validated_data['payment']['payload'],
                        amount=int(charge_amount * 100),
                        currency=settings.CURRENCY,
                        receipt_email=user.email
                    )
                except stripe.StripeError as exc:
                    raise exceptions.PaymentDenied()

                purchase_transaction = models.Transaction.objects.create(
                    amount=charge_amount,
                    stripe_charge=charge.id
                )
                response_data['transactions'].append(purchase_transaction)

                for ticket in safe_tickets:
                    ticket.pending = False
                    purchase_transaction.ticket_ownerships.add(
                        ticket.ownerships.latest())
                    ticket.save()
                    response_data['tickets'].append(ticket)



        return response_data


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Ticket
        fields = [
            'url',
            'ticket_type',
            'variation_choices',
            'utilized'
        ]


class VariationChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VariationChoice
        fields = [
            'url',
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
