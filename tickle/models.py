import logging
import uuid
from collections import OrderedDict
from decimal import Decimal
from os import urandom
from binascii import hexlify
import json
from base64 import b64encode
from six import BytesIO

import requests
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _, ugettext
from model_utils.managers import InheritanceQuerySetMixin
from templated_email import send_templated_mail, InlineImage
from sesam import SesamError, SesamStudentNotFound
import qrcode

from .utils import signing
from tickle.db.fields import NameField, SlugField, DescriptionField, \
    MoneyField, NullCharField, IdField
from tickle.utils.email import generate_pretty_email

logger = logging.getLogger(__name__)


def generate_code(length):
    # Returns a random hex string, `length` characters long.
    return hexlify(urandom(length // 2 + (length % 2 > 0)))[0:length].decode()


def generate_ticket_ownership_code():
    return generate_code(6)


class ConditionQuerySet(InheritanceQuerySetMixin, models.QuerySet):
    def met(self, person):
        met_pks = []

        for condition in self.select_subclasses():
            if condition.is_met(person):
                met_pks.append(condition.pk)

        return self.filter(pk__in=met_pks)


class TicketTypeQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def unpublished(self):
        return self.filter(is_published=False)

    def generally_available(self):
        return self.filter(is_generally_available=True)


class TicketQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(pending=True)

    def unpending(self):
        return self.filter(pending=False)

    def owned_by(self, user, only_current=True):
        ownerships = TicketOwnership.objects

        if only_current:
            ownerships = (ownerships
                          .order_by('ticket_id', '-created')
                          .distinct('ticket_id'))

        return self.filter(
            ownerships__in=ownerships.filter(user=user)
        ).distinct()  # Buying, reselling and buying back would give duplicates

    def before_in_queue(self, ticket):
        # Get the ticket's position by purchase time. In the extreme
        # case of multiple tickets purchased in the same
        # *microsecond*, we let the id (and since we use random
        # UUIDs, luck) decide. Since the position is based on
        # creation time, it can never get higher during the
        # transaction, but it can get lower (if pending tickets
        # disappear due to failed payments).
        return self.filter(Q(created__lt=ticket.created) |
                           Q(created__exact=ticket.created, pk__lt=ticket.pk))

    def email_ticket(self):
        for i in self:
            i.email_ticket()


@python_2_unicode_compatible
class Condition(models.Model):
    id = IdField()

    active = models.BooleanField(
        default=True,
        verbose_name=_('active'),
        help_text=_('Determines whether the condition should be displayed and '
                    'included in queries.'))

    objects = ConditionQuerySet.as_manager()

    type_str = _('Condition')

    class Meta:
        verbose_name = _('condition')
        verbose_name_plural = _('conditions')

    def __str__(self):
        return '{0}: {1}'.format(self.type_str, self.condition_str)

    @property
    def condition_str(self):
        return ''

    def is_met(self, user):
        raise Exception('is_met method not overridden or incorrectly called.')


class StudentUnionMemberCondition(Condition):
    student_union = models.ForeignKey(
        'StudentUnion',
        related_name='+',
        verbose_name=_('student union'))

    type_str = ugettext('Student union member')

    class Meta:
        verbose_name = _('student union member condition')
        verbose_name_plural = _('student union member conditions')

    @property
    def condition_str(self):
        return '{}'.format(self.student_union)

    def is_met(self, user):
        return user.student_union_id == self.student_union_id


class EventQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Event(models.Model):
    id = IdField()

    name = NameField()
    slug = SlugField(
        unique_with='organization__slug',
        populate_from='name',
        editable=True)
    description = DescriptionField()

    organization = models.ForeignKey(
        'Organization',
        related_name='events',
        verbose_name=_('organization'))

    published = models.BooleanField(
        default=True,
        verbose_name=_('published'))

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('name',)
        unique_together = [
            ['organization', 'name'],
            ['organization', 'slug']
        ]

        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return self.name


class ModifierQuerySet(models.QuerySet):
    def eligible(self, user, force_reevaluation=False):
        if user.is_anonymous():
            return self.none()

        return self.filter(condition__in=user.get_met_conditions(
            force_reevaluation=force_reevaluation))

    def delta(self):
        return self.aggregate(delta=models.Sum('delta'))['delta'] or Decimal('0.00')


class Modifier(models.Model):
    id = IdField()

    condition = models.ForeignKey(
        'Condition',
        related_name='modifiers',
        verbose_name=_('condition'))
    ticket_type = models.ForeignKey(
        'TicketType',
        related_name='modifiers',
        verbose_name=_('product'))

    delta = MoneyField(
        verbose_name=_('delta'),
        help_text=_('For discount, enter a negative value.'))

    objects = ModifierQuerySet.as_manager()

    class Meta:
        unique_together = [
            ['condition', 'ticket_type']
        ]

        verbose_name = _('modifier')
        verbose_name_plural = _('modifiers')

    @property
    def condition_subclass(self):
        return Condition.objects.get_subclass(id=self.condition_id)


class Organization(models.Model):
    id = IdField()

    name = NameField(
        unique=True)
    slug = SlugField(
        unique=True,
        populate_from='name')

    organization_number = models.CharField(
        max_length=12,
        verbose_name=_('organization number'))

    address = models.TextField(
        verbose_name=_('address'))

    email = models.EmailField(
        verbose_name=_('email address'))

    admins = models.ManyToManyField(
        'User',
        related_name='admin_for_organizers',
        verbose_name=_('admins'))

    stripe_authorized = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Stripe authorization timestamp'))
    stripe_live_mode = models.BooleanField(
        default=False,
        verbose_name=_('Stripe live mode'))
    stripe_account_id = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe account ID'))
    stripe_refresh_token = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe refresh token'))
    stripe_public_key = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe public key'))
    stripe_secret_key = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe secret key'))
    stripe_read_only = models.BooleanField(
        default=True,
        verbose_name=_('Stripe read only access'))

    class Meta:
        permissions = [
            ['manage_organization_stripe', _('Can manage Stripe for organization')]
        ]

    def __str__(self):
        return self.name

    def authorize_stripe(self, code):
        response = requests.post(settings.STRIPE_OAUTH_TOKEN_URL, {
            'client_secret': settings.STRIPE_SECRET_KEY,
            'grant_type': 'authorization_code',
            'code': code})

        # Makes sure we won't miss any error.
        response.raise_for_status()

        response_data = response.json()
        self.stripe_authorized = now()
        self.stripe_live_mode = response_data['livemode']
        self.stripe_account_id = response_data['stripe_user_id']
        self.stripe_refresh_token = response_data['refresh_token']
        self.stripe_public_key = response_data['stripe_publishable_key']
        self.stripe_secret_key = response_data['access_token']
        self.stripe_read_only = response_data['scope'] == 'read_only'
        self.save()


class Transaction(models.Model):
    created = models.DateTimeField(
        default=now,
        verbose_name=_('created'))
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('amount'))
    stripe_charge = models.CharField(
        max_length=64,
        verbose_name=_('Stripe charge'))

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')


class UserQuerySet(models.QuerySet):
    def pretty_emails_string(self):
        """
        Returns a string with pretty formatted emails, separated by semicolons
        """

        recipient_list = ''
        values = self.values('name', 'email')

        for i in values:
            recipient_list += generate_pretty_email(i['name'], i['email'])

        return recipient_list


class UserManager(models.Manager.from_queryset(UserQuerySet),
                  BaseUserManager):
    def create_user(self, email, name=None, fullname=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if fullname:
            # This is kind of a hack to adapt to python-social-auth.
            name = fullname

        if not name:
            raise ValueError('Users must have a name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin, models.Model):
    id = IdField()

    name = NameField()

    student_union = models.ForeignKey(
        'StudentUnion',
        related_name='members',
        null=True,
        blank=True,
        verbose_name=_('student union'))

    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name=_('email address'))

    nin = NullCharField(
        max_length=12,
        verbose_name=_('national identity number'))

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is active'))
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is staff'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ['name']

        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return '{} ({})'.format(self.get_full_name(), self.email)

    @property
    def is_liu_student(self):
        return self.email.endswith('@student.liu.se')

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def get_met_conditions(self, force_reevaluation=False):
        cache_key = 'people.person.{}.met_conditions'.format(self.pk)
        conditions = cache.get(cache_key)
        if force_reevaluation or conditions is None:
            conditions = Condition.objects.met(person=self)
            cache.set(cache_key, conditions,
                      timeout=settings.CACHE_TIMEOUT_PERSON_CONDITIONS)
        return conditions

    @property
    def pretty_email(self):
        return generate_pretty_email(self.name, self.email)


class StudentUnion(models.Model):
    id = IdField()
    name = NameField(unique=True)

    class Meta:
        verbose_name = _('student union')
        verbose_name_plural = _('student unions')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Ticket(models.Model):
    id = IdField()

    ticket_type = models.ForeignKey(
        'TicketType',
        related_name='tickets',
        verbose_name=_('ticket type'))
    variation_choices = models.ManyToManyField(
        'VariationChoice',
        blank=True,
        related_name='tickets',
        verbose_name=_('variation choices'))

    access_code = models.ForeignKey(
        'AccessCode',
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name=_('access code'),
        help_text=_('The access code used to buy this ticket, if any.'))

    pending = models.BooleanField(
        default=False,
        verbose_name=_('pending'))

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created'))
    utilized = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('utilized'))

    objects = TicketQuerySet.as_manager()

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __str__(self):
        return '{0}'.format(self.ticket_type)

    def utilize(self):
        self.utilized = now()

    def unutilize(self):
        self.utilized = None


class TicketOwnership(models.Model):
    id = IdField()

    # This can be changed to invalidate generated switch links.
    code = models.CharField(
        max_length=16,
        default=generate_ticket_ownership_code,
        verbose_name=_('code'))

    ticket = models.ForeignKey(
        'Ticket',
        related_name='ownerships',
        verbose_name=_('ticket'))
    user = models.ForeignKey(
        'User',
        related_name='ticket_ownerships',
        verbose_name=_('user'))

    modifiers = models.ManyToManyField(
        'Modifier',
        related_name='ticket_ownerships',
        blank=True,
        verbose_name=_('utilized modifiers'))

    transactions = models.ManyToManyField(
        'Transaction',
        related_name='ticket_ownerships',
        blank=True,
        verbose_name=_('transactions'))

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created'))

    class Meta:
        get_latest_by = 'created'

        verbose_name = _('ticket ownership')
        verbose_name_plural = _('ticket ownerships')

    def save(self, *args, **kwargs):
        # self._state.adding is always False after save()
        first_save = self._state.adding

        super(TicketOwnership, self).save(*args, **kwargs)

        # Automatically add modifiers *only* on first save()
        if first_save:
            self.modifiers.set(
                # We force reevaluate when the real shit is going down (i.e.
                # now) to ensure we don't get inconsistencies
                self.ticket.ticket_type.modifiers.eligible(
                    self.user, force_reevaluation=True
                )
            )

    @property
    def price(self):
        assert self.pk is not None, 'Save before calculating the price.'

        return (self.ticket.ticket_type.price +
                self.modifiers.delta() +
                self.ticket.variation_choices.delta())

    @property
    def is_current(self):
        return self == self.ticket.ownerships.latest()

    @property
    def resell_token(self):
        return signing.dumps(OrderedDict((('id', str(self.id)), ('code', self.code))), salt='resell_token')

    def email_confirmation(self):
        qr_inline = InlineImage(filename='qr.png', content=self.get_qr_raw())
        send_templated_mail(
            template_name='ticket_ownership_new',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.user.pretty_email],
            context={
                'domain': Site.objects.get_current().domain,
                'ticket_ownership': self,
                'qr': qr_inline
            }
        )

    def get_qr_raw(self):
        output_buffer = BytesIO()
        qr_image = qrcode.make(
            json.dumps(
                OrderedDict((('id', str(self.id)), ('code', self.code)))),
            error_correction=qrcode.ERROR_CORRECT_H,
            box_size=6,
            border=4  # The QR spec stipulates a border of 4
        )
        qr_image.save(output_buffer, format='png', optimize=True)
        return output_buffer.getvalue()

    def get_qr(self):
        return b64encode(self.get_qr_raw())


class AccessCodeQuerySet(models.QuerySet):
    def get(self, *args, token=None, **kwargs):
        if token:
            return self.get_by_token(token)

        return super(AccessCodeQuerySet, self).get(*args, **kwargs)

    def get_by_token(self, token):
        return self.get(id=signing.loads(token, salt='access_code'))

    def utilizable(self):
        return self.filter(tickets__isnull=True)


class AccessCode(models.Model):
    id = IdField()

    ticket_type = models.ForeignKey('TicketType')

    objects = AccessCodeQuerySet.as_manager()

    class Meta:
        verbose_name = _('access code')
        verbose_name_plural = _('access codes')

    def __str__(self):
        return self.token

    @property
    def token(self):
        return signing.dumps(self.id.hex, salt='access_code')

    @property
    def is_utilizable(self):
        return not self.tickets.exists()


class TicketType(models.Model):
    id = IdField()
    index = models.PositiveIntegerField(default=1)

    name = NameField()
    description = DescriptionField()

    event = models.ForeignKey(
        'Event',
        related_name='ticket_types',
        verbose_name=_('event'))

    price = MoneyField(
        verbose_name=_('price'))

    conflicts_with = models.ManyToManyField(
        'self',
        blank=True,
        related_name='*',
        verbose_name=_('conflicts with'))
    # upgradable_to = models.ManyToManyField(
    #     'self',
    #     related_name='downgradable_to')

    is_published = models.BooleanField(
        default=True,
        verbose_name=_('published'))
    is_generally_available = models.BooleanField(
        default=False,
        verbose_name=_('generally available for purchase'))

    max_personal_quantity = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name=_('maximum personal quantity'),
        help_text=_('Blank means no limit.'))
    max_total_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('maximum total quantity'),
        help_text=_('Blank means no limit.'))

    objects = TicketTypeQuerySet.as_manager()

    class Meta:
        ordering = ('index', 'name')
        verbose_name = _('ticket type')
        verbose_name_plural = _('ticket types')

    def __str__(self):
        return self.name

    @property
    def within_max_total_quantity(self):
        if self.max_total_quantity is None:
            return True
        return self.tickets.unpending().count() < self.max_total_quantity

    def modifier_delta(self, user):
        return self.modifiers.eligible(user).delta()


class Variation(models.Model):
    id = IdField()
    index = models.PositiveIntegerField(default=1)
    name = NameField()

    ticket_type = models.ForeignKey(
        'TicketType',
        related_name='variations',
        verbose_name=_('ticket type'))

    class Meta:
        ordering = ('index', 'name')
        unique_together = [
            ['name', 'ticket_type']
        ]
        verbose_name = _('variation')
        verbose_name_plural = _('variations')

    def __str__(self):
        return self.name


class VariationChoiceQuerySet(models.QuerySet):
    def delta(self):
        return (self.aggregate(delta=models.Sum('delta'))['delta']
                or Decimal('0.00'))


class VariationChoice(models.Model):
    id = IdField()
    index = models.PositiveIntegerField(default=1)
    name = NameField()
    delta = MoneyField(
        default=0,
        verbose_name=_('delta'),
        help_text=_('For discount, enter a negative value.'))
    variation = models.ForeignKey(
        'Variation',
        related_name='choices',
        verbose_name=_('variation'))

    objects = VariationChoiceQuerySet.as_manager()

    class Meta:
        ordering = ('index',)
        unique_together = [
            ['name', 'variation']
        ]
        verbose_name = _('variation choice')
        verbose_name_plural = _('variation choices')

    def __str__(self):
        return self.name


def social_get_union(response, details, backend, *args, **kwargs):
    if backend.name != 'liu':
        # Just pass
        return

    union = None

    try:
        union = settings.SESAM_STUDENT_SERVICE_CLIENT.get_student(
            nor_edu_person_lin=response.get('nor_edu_person_lin')).union
    except SesamStudentNotFound:
        pass
    except SesamError:
        logger.warning('Sesam request failed', exc_info=True)

    details['student_union'] = (StudentUnion.objects.get_or_create(name=union)[0]
                                if union else None)

    return {'details': details}
