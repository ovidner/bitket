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

    def validate(self, attrs):
        if attrs['ticket_type'].variations.exclude(choices__in=attrs['variation_choices']).exists():
            raise exceptions.InvalidVariationChoices(_('At least one variation choice is missing.'))
        if models.VariationChoice.objects.filter(id__in=attrs['variation_choices']).exclude(variation__ticket_type=attrs['ticket_type']).exists():
            raise exceptions.InvalidVariationChoices(
                _('At least one variation choice belongs to a variation of another ticket type than the one supplied.'))
        if attrs['ticket_type'].variations.filter(choices__in=attrs['variation_choices']).distinct().count() != len(attrs['variation_choices']):
            raise exceptions.InvalidVariationChoices(_('At least two variation choices belongs to the same variation.'))
        return attrs


class PurchaseTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Transaction
        fields = (
            'amount',
        )


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
        queryset=models.AccessCode.objects.all(),
        allow_empty=True)
    payment = PurchasePaymentSerializer(
        write_only=True)
    user = PurchaseUserSerializer(
        write_only=True)

    # Response only
    messages = serializers.ListField(
        read_only=True,
        child=serializers.CharField(),
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

        # Use a transaction with weak isolation? Well, it was the only way I
        # could come up with that guaranteed a fair creation order of tickets
        # while still making sure that the only tickets committed to the
        # database are the actual, purchased tickets. But most importantly, this
        # should also save us from a few possible nasty race conditions, leading
        # to too many sold tickets.
        #
        # The trick is to only perform actions on the tickets that have a clear
        # destiny and to wait for the ones that does not have that.
        with transaction.atomic(using=settings.READ_UNCOMMITTED_ISOLATION):
            unclear_tickets = set()
            safe_tickets = set()
            lost_tickets = set()

            # Creates all ticket objects right away to ensure a reasonably fair
            # position in the queue. We'll do all necessary validations later
            # on.
            for ticket_data in tickets_data:
                for access_code in validated_data.get('access_codes'):
                    if access_code and access_code.ticket_type == ticket_data.ticket_type:
                        ticket_data['access_code'] = access_code
                ticket = models.Ticket.objects.create(pending=True, **ticket_data)
                models.TicketOwnership.objects.create(ticket=ticket, user=user)
                unclear_tickets.add(ticket)

            while True:
                for ticket in unclear_tickets:
                    # Unpublished ticket type
                    if not ticket.ticket_type.is_published:
                        lost_tickets.add(ticket)
                        response_data['messages'].append(OrderedDict((
                            ('code', 'ticket_type_unpublished'),
                            ('text', _("The ticket type {} is not published.".format(ticket.ticket_type.name))),
                            ('entity', reverse('tickettype-detail', kwargs={'pk': ticket.ticket_type_id}))
                        )))
                        continue

                    if not ticket.ticket_type.is_generally_available:
                        # Ticket type not available for purchase
                        if not ticket.access_code:
                            lost_tickets.add(ticket)
                            response_data['messages'].append(OrderedDict((
                                ('code', 'ticket_type_unavailable'),
                                ('text', _(
                                    "The ticket type '{}' is not available for purchase.".format(
                                        ticket.ticket_type.name))),
                                ('entity', reverse('tickettype-detail', kwargs={
                                    'pk': ticket.ticket_type_id}))
                            )))
                            continue

                        # Access code is supplied, has an impact on availability
                        # and is utilized by a ticket before this one.
                        if ticket.access_code and ticket.access_code.tickets.filter(
                            # See below on how we determine positions.
                            Q(created__lt=ticket.created) |
                            Q(created__exact=ticket.created, pk__lt=ticket.pk)
                        ).exists():
                            lost_tickets.add(ticket)
                            response_data['messages'].append(OrderedDict((
                                ('code', 'access_code_utilized'),
                                ('text', _("The access code is already utilized."))
                            )))
                            continue

                    # No tickets left
                    if not ticket.ticket_type.within_max_total_quantity:
                        lost_tickets.add(ticket)
                        response_data['messages'].append(OrderedDict((
                            ('code', 'ticket_type_quantitatively_unavailable'),
                            ('text', _("There are no tickets of the type '{}' left.".format(ticket.ticket_type.name))),
                            ('entity', reverse('tickettype-detail', kwargs={'pk': ticket.ticket_type_id}))
                        )))
                        continue

                    if ticket.ticket_type.max_personal_quantity and ticket.ticket_type.tickets.filter(
                        Q(created__lt=ticket.created) |
                        Q(created__exact=ticket.created, pk__lt=ticket.pk)
                    ).owned_by(user).count() >= ticket.ticket_type.max_personal_quantity:
                        lost_tickets.add(ticket)
                        response_data['messages'].append(OrderedDict((
                            ('code', 'ticket_type_personal_limit_reached'),
                            ('text', _(
                                "You have reached your personal limit for the ticket type '{}'.".format(
                                    ticket.ticket_type.name))),
                            ('entity', reverse('tickettype-detail', kwargs={
                                'pk': ticket.ticket_type_id}))
                        )))
                        continue

                    # Get the ticket's position by purchase time. In the extreme
                    # case of multiple tickets purchased in the same
                    # *microsecond*, we let the id (and since we use random
                    # UUIDs, luck) decide. Since the position is based on
                    # creation time, it can never get higher during the
                    # transaction, but it can get lower (if pending tickets
                    # disappear due to failed payments).
                    position = ticket.ticket_type.tickets.filter(
                        Q(created__lt=ticket.created) |
                        Q(created__exact=ticket.created, pk__lt=ticket.pk)
                    ).count()

                    # position is zero-indexed
                    if position < ticket.ticket_type.total_limit:
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

                charge = stripe.Charge.create(
                    stripe_account=organization.stripe_account_id,
                    source=validated_data['payment']['payload'],
                    amount=int(charge_amount * 100),
                    currency=settings.CURRENCY
                )

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

        user.nin = validated_data.get('user').nin
        user.save()

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
            'delta'
        ]


class VariationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Variation
        fields = [
            'url',
            'ticket_type',
            'name'
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
            'is_utilizable'
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
