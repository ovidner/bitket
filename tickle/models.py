import uuid
from _pydecimal import Decimal

import requests
import stripe
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _, ugettext
from dry_rest_permissions.generics import allow_staff_or_superuser, \
    authenticated_users
from model_utils.managers import InheritanceQuerySetMixin
from templated_email import send_templated_mail
from tickle.common.behaviors import NameSlugMixin, NameSlugDescriptionMixin, \
    NameMixin
from tickle.products.querysets import logger

from tickle import products
from tickle.common import exceptions
from tickle.db.fields import NameField, SlugField, DescriptionField, \
    MoneyField, NullCharField, PasswordField
from tickle.exceptions import ConflictingProductVariationChoices
from tickle.fields import PidField
from tickle.utils import KobraClient, Unauthorized, StudentNotFound
from tickle.utils import generate_pretty_email


class Model(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'))

    class Meta:
        abstract = True

    @staticmethod
    def has_read_permission(request):
        # Use this method only to explicitly deny permissions.
        return True

    @staticmethod
    def has_write_permission(request):
        # Use this method only to explicitly deny permissions.
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_create_permission(request):
        return False

    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_object_destroy_permission(self, request):
        # Explicitly defined. No object should be user removable by default.
        return False


@python_2_unicode_compatible
class Condition(Model):
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

    def is_met(self, person):
        raise Exception('is_met method not overridden or incorrectly called.')


class StudentUnionMemberCondition(Condition):
    student_union = models.ForeignKey(
        'people.models.py',
        related_name='+',
        verbose_name=_('student union'))

    type_str = ugettext('Student union member')

    class Meta:
        verbose_name = _('student union member condition')
        verbose_name_plural = _('student union member conditions')

    @property
    def condition_str(self):
        return '{}'.format(self.student_union)

    def is_met(self, person):
        return person.student_union_id == self.student_union_id


class EventQuerySet(models.QuerySet):
    def holdings(self):
        return Holding.objects.filter(product__ticket_type__events__in=self)

    def visitors(self):
        return self.holdings().purchased().holders()

    def organizers(self):
        return Organizer.objects.filter(events__in = self).distinct()


@python_2_unicode_compatible
class MainEvent(Model):
    name = NameField()
    slug = SlugField(
        unique_with='organizer__slug',
        populate_from='name',
        editable=True)
    description = DescriptionField()

    organizer = models.ForeignKey(
        'organizers.models.py',
        related_name='events',
        verbose_name=_('organizer'))

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('name',)
        unique_together = [
            ['organizer', 'name'],
            ['organizer', 'slug']
        ]

        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return self.name


class ProductModifierQuerySet(models.QuerySet):
    def eligible(self, person, force_reevaluation=False):
        if person.is_anonymous():
            return self.none()

        return self.filter(condition__in=person.get_met_conditions(
            force_reevaluation=force_reevaluation))

    def delta(self):
        return self.aggregate(delta=models.Sum('delta_amount'))['delta'] or Decimal('0.00')


class ProductModifier(Model):
    condition = models.ForeignKey(
        '...models.Condition',
        related_name='product_modifiers',
        verbose_name=_('condition'))
    product = models.ForeignKey(
        'products.models.py',
        related_name='product_modifiers',
        verbose_name=_('product'))

    delta_amount = MoneyField(
        verbose_name=_('delta (amount)'),
        help_text=_('For discount, enter a negative value.'))

    objects = ProductModifierQuerySet.as_manager()

    class Meta:
        unique_together = [
            ['condition', 'product']
        ]

        verbose_name = _('product modifier')
        verbose_name_plural = _('product modifiers')

    def delta(self):
        return self.delta_amount

    @property
    def condition_subclass(self):
        return Condition.objects.get_subclass(id=self.condition_id)


class HoldingModifier(Model):
    product_modifier = models.ForeignKey(
        'ProductModifier',
        related_name='holding_modifiers',
        verbose_name=_('product modifier'))
    holding = models.ForeignKey(
        'products.models.py',
        related_name='holding_modifiers',
        verbose_name=_('holding'))

    class Meta:
        unique_together = [
            ['product_modifier', 'holding']
        ]

        verbose_name = _('holding modifier')
        verbose_name_plural = _('holding modifiers')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.holding.product == self.product_modifier.product:
            raise ValidationError('Impossible holding/modifier combination. '
                                  'Products not matching.')

        super(HoldingModifier, self).save(force_insert, force_update, using,
                                          update_fields)


class OrganizerStripeMixin(models.Model):
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
        abstract = True

        permissions = [
            ['manage_organizer_stripe', _('Can manage Stripe for organizer')]
        ]

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


class Organizer(NameSlugMixin, OrganizerStripeMixin, Model):
    name = NameField(
        unique=True)
    slug = SlugField(
        unique=True,
        populate_from='name')

    admins = models.ManyToManyField(
        'people.models.py',
        related_name='admin_for_organizers',
        verbose_name=_('admins'))

    class Meta:
        pass


class Transaction(Model):
    timestamp = models.DateTimeField(
        default=now,
        verbose_name=_('timestamp'))
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('amount'))
    stripe_charge = models.CharField(
        max_length=64,
        verbose_name=_('Stripe charge'))
    cart = models.ForeignKey(
        'products.models.py',
        verbose_name=_('cart'))
    organizer = models.ForeignKey(
        '...models.Organizer',
        verbose_name=_('organizer'))

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')


class PidMixin(models.Model):
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('birth date'))
    pid_code = NullCharField(
        max_length=4,
        verbose_name=_('national identity code'),
        help_text=_('Last 4 digits in Swedish national identity number.'))
    pid_coordination = models.BooleanField(
        default=False,
        verbose_name=_('coordination number'),
        help_text=_('Designates if national identity number is a '
                    '<em>samordningsnummer</em>.'))

    class Meta:
        abstract = True

    def _get_pid(self):
        if self.birth_date:
            day = self.birth_date.day

            if self.pid_coordination:
                day += 60

            return '{0:0>4}{1:0>2}{2:0>2}-{3}'.format(
                self.birth_date.year,
                self.birth_date.month,
                day,
                self.pid_code or '0000',
            )
        else:
            return None

    def _set_pid(self, value):
        self.birth_date, self.pid_code, self.pid_coordination = PidField().clean(value)

    pid = property(_get_pid, _set_pid)


class PasswordFieldMixin(object):
    """
    Placed in a mixin since we can't override a Django field.
    """
    password = PasswordField()


class PersonQuerySet(models.QuerySet):
    def fill_kobra_data(self):
        for i in self:
            i.fill_kobra_data(save=True, overwrite_name=False, fail_silently=True)

    def pretty_emails_string(self):
        """
        Returns a string with pretty formatted emails, separated by semicolons
        """

        recipient_list = ''
        values = self.values('first_name', 'last_name', 'email')

        for i in values:
            recipient_list += generate_pretty_email(i['first_name'], i['last_name'], i['email'])

        return recipient_list


class PersonManager(models.Manager.from_queryset(PersonQuerySet),
                    BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name, last_name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class Person(PidMixin, AbstractBaseUser, PermissionsMixin,
             Model):
    first_name = NameField(
        verbose_name=_('first name'))
    last_name = NameField(
        verbose_name=_('last name'))

    liu_id = NullCharField(
        max_length=8,
        unique=True,
        verbose_name=_('LiU ID'))
    liu_card_rfid = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_('LiU card number'))
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

    special_nutrition = models.ManyToManyField(
        'SpecialNutrition',
        blank=True,
        verbose_name=_('special nutrition'),
        help_text=_('Specify any special nutritional needs or habits.'))

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is active'))
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is staff'))

    objects = PersonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        unique_together = [
            # If both are specified, the combination must be unique. Two birth
            # dates with NULL as pid_code should pass as we want it to.
            ['birth_date', 'pid_code', 'pid_coordination']
        ]
        ordering = ['first_name', 'last_name']

        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __str__(self):
        return self.get_full_name()

    @staticmethod
    @authenticated_users
    def has_current_permission(request):
        return True

    def has_object_read_permission(self, request):
        return request.user == self

    def has_object_write_permission(self, request):
        return request.user == self

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return '{} {}.'.format(self.first_name, self.last_name[0])

    def get_met_conditions(self, force_reevaluation=False):
        cache_key = 'people.person.{}.met_conditions'.format(self.pk)
        conditions = cache.get(cache_key)
        if force_reevaluation or conditions is None:
            conditions = Condition.objects.met(person=self)
            cache.set(cache_key, conditions,
                      timeout=settings.CACHE_TIMEOUT_PERSON_CONDITIONS)
        return conditions

    def get_kobra_data(self, fail_silently=False):
        """
        Searches the KOBRA database by the person's attributes in the following
        order:

            1. LiU ID
            2. PID
            3. RFID card number

        Returns a dictionary.
        """

        request = dict()
        if self.liu_id:
            request = {'liu_id': self.liu_id}
        elif self.birth_date and self.pid_code:
            request = {'personal_number': self.pid}
        elif self.liu_card_rfid:
            request = {'rfid_number': self.liu_card_rfid}
        else:
            if fail_silently:
                return
            else:
                raise KeyError('Person object must have LiU id, PID or RFID '
                               'card number defined.')

        data = KobraClient().get_student(**request)

        return data

    def fill_kobra_data(self, save=False, overwrite_name=False, fail_silently=False):
        try:
            data = self.get_kobra_data(fail_silently=fail_silently)
        except (Unauthorized, StudentNotFound) as e:
            if fail_silently:
                return
            raise e

        if data:
            # Now we trust KOBRA to always give us all values. Let's hope it works that way.

            if not self.first_name or overwrite_name:
                self.first_name = data['first_name']
            if not self.last_name or overwrite_name:
                self.last_name = data['last_name']

            # We always overwrite these.
            self.pid = data['personal_number']
            self.liu_id = data['liu_id']
            self.liu_card_rfid = data['rfid_number'] or ''  # Some people actually have no LiU card

            if data['union']:
                self.student_union = StudentUnion.objects.get_or_create(name=data['union'])[0]

            if save:
                self.save()

        return self

    @property
    def pretty_email(self):
        return generate_pretty_email(self.first_name, self.last_name, self.email)

    def create_default_cart(self):
        if not self.default_cart:
            self.carts.create(person=self)

    @property
    def default_cart(self):
        return self.carts.get_or_create(person=self, purchased=None)[0]


@python_2_unicode_compatible
class SpecialNutrition(Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    class Meta:
        ordering = ['name']

        verbose_name = _('special nutrition')
        verbose_name_plural = _('special nutritions')

    def __str__(self):
        return self.name


class StudentUnion(NameSlugMixin, Model):
    name = NameField(unique=True)
    slug = SlugField(unique=True, populate_from='name')

    class Meta:
        verbose_name = _('student union')
        verbose_name_plural = _('student unions')


@python_2_unicode_compatible
class Cart(Model):
    person = models.ForeignKey(
        '...models.Person',
        related_name='carts',
        verbose_name=_('person'))
    purchased = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('purchased'))

    objects = CartQuerySet.as_manager()

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return '{}'.format(self.person)

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return request.user == self.person

    def has_object_purchase_permission(self, request):
        return request.user == self.person and not self.purchased

    def purchase(self, stripe_token):
        self.holdings.prepare_for_purchase()
        # This is ugly. fixme!
        if self.person.holdings.quantity() > 1:
            raise exceptions.EventProductLimitExceeded()
        self.purchased = now()
        self.save()
        self.holdings.charge(self, stripe_token)
        self.holdings.email_ticket()


@python_2_unicode_compatible
class Holding(Model):
    person = models.ForeignKey(
        '...models.Person',
        related_name='holdings',
        verbose_name=_('person'))
    product = models.ForeignKey(
        'Product',
        related_name='holdings',
        verbose_name=_('product'))
    product_variation_choices = models.ManyToManyField(
        'ProductVariationChoice',
        related_name='holdings',
        verbose_name=_('product variation choices'))
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('quantity'))

    cart = models.ForeignKey(
        'Cart',
        related_name='holdings',
        verbose_name=_('cart'))

    utilized = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('utilized'))

    purchase_price = MoneyField(
        null=True,
        blank=True,
        verbose_name=_('purchase price'))

    objects = HoldingQuerySet.as_manager()

    class Meta:
        verbose_name = _('holding')
        verbose_name_plural = _('holdings')

    def __str__(self):
        return u'{0} {1}'.format(self.product, self.person)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self._has_conflicting_product_variation_choices():
            raise ConflictingProductVariationChoices(
                _('Holding has conflicting product variation choices.'))

        super(Holding, self).save(force_insert, force_update, using,
                                  update_fields)

    @staticmethod
    def has_create_permission(request):
        return True

    def _user_is_organizer_admin(self, user):
        return self.product.main_event.organizer.admins.filter(
            pk=user.pk).exists()

    def has_object_read_permission(self, request):
        return (request.user == self.person or
                request.user == self.cart.person or
                self._user_is_organizer_admin(request.user))

    def has_object_write_permission(self, request):
        return self.has_object_read_permission(request) and not self.is_purchased

    def has_object_utilize_permission(self, request):
        return self._user_is_organizer_admin(request.user)

    def has_object_unutilize_permission(self, request):
        return self.has_object_utilize_permission(request)

    def has_object_destroy_permission(self, request):
        return self.has_object_write_permission(request)

    def _will_modify_purchased_holding(self):
        return self.cart.purchased

    def _will_exceed_total_limit(self):
        if self.product.total_limit is None:
            return False
        return (self.product.holdings.purchased().quantity() + self.quantity) > self.product.total_limit

    def _will_exceed_personal_limit(self):
        if self.product.personal_limit is None:
            return False
        return (self.product.holdings.filter(person=self.person).purchased().quantity() + self.quantity) > self.product.personal_limit

    def _has_conflicting_product_variation_choices(self):
        if not self.pk:
            return False
        return self.product_variation_choices.values(
            'variation').annotate(count=models.Count('id')).order_by().filter(
            count__gt=1).exists()

    def email_ticket(self):
        send_templated_mail(
            template_name='holding',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.person.pretty_email],
            context={
                'domain': Site.objects.get_current().domain,
                'holding': self,
            }
        )

    def utilize(self):
        self.utilized = now()

    def unutilize(self):
        self.utilized = None

    #The final price of the holding.
    #Should only be used when all ProducVariationChoices have been added properly
    @property
    def price(self):
        return self.product.base_price + self.product.modifier_delta(self.person) + self.product_variation_choices.delta()

    #Creates HoldingModifiers for the holding, and sets purchase_price
    def prepare_for_purchase(self, ignore_limits=False, modify_history_allowed=False):
        if not ignore_limits and self._will_exceed_total_limit():
            raise exceptions.TotalProductLimitExceeded()
        if not ignore_limits and self._will_exceed_personal_limit():
            raise exceptions.PersonalProductLimitExceeded()
        if not modify_history_allowed and self.is_purchased:
            raise exceptions.ModifiesHistory()

        eligible_product_modifiers = self.product.product_modifiers.eligible(
            self.person, force_reevaluation=True)
        for product_modifier in eligible_product_modifiers:
            HoldingModifier.objects.create(product_modifier=product_modifier,
                                           holding=self)
        self.purchase_price = self.price
        self.save()

    @property
    def is_purchased(self):
        return self.cart.purchased is not None

    @property
    def total(self):
        return self.price * self.quantity


class Product(NameSlugDescriptionMixin, Model):
    name = NameField()
    slug = SlugField()
    description = DescriptionField()

    main_event = models.ForeignKey(
        '...models.MainEvent',
        related_name='products',
        verbose_name=_('main event'))

    base_price = MoneyField(
        verbose_name=_('base price'))

    published = models.BooleanField(
        default=True,
        verbose_name=_('published'))
    personal_limit = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name=_('personal limit'),
        help_text=_('Blank means no limit.'))
    total_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_('total limit'),
        help_text=_('Blank means no limit.'))
    transferable = models.BooleanField(
        default=True,
        verbose_name=_('transferable'),
        help_text=_('If people should be able to transfer this product to '
                    'other people.'))

    objects = ProductQuerySet.as_manager()

    class Meta:
        unique_together = [
            ['main_event', 'name'],
            ['main_event', 'slug']
        ]
        ordering = ['name']
        verbose_name = _('product')
        verbose_name_plural = _('products')

    @property
    def is_available(self):
        if self.total_limit is None:
            return True
        return self.holdings.purchased().quantity() < self.total_limit

    def modifier_delta(self, person):
        return self.product_modifiers.eligible(person).delta()

    def has_reached_limit(self):
        return self.limit and self.holdings.purchased().quantity() >= self.limit


class ProductVariation(NameMixin, Model):
    name = NameField()

    product = models.ForeignKey(
        'Product',
        related_name='variations',
        verbose_name=_('product'))

    class Meta:
        ordering = ['name']
        unique_together = [
            ['name', 'product']
        ]
        verbose_name = _('product variation')
        verbose_name_plural = _('product variations')

    def __str__(self):
        return '{} > {}'.format(self.product, self.name)


class ProductVariationChoiceQuerySet(models.QuerySet):
    def delta(self):
        return self.aggregate(delta=models.Sum('delta_amount'))['delta'] or Decimal('0.00')


class ProductVariationChoice(NameMixin, Model):
    name = NameField()
    order = models.PositiveIntegerField(verbose_name=_('order'))
    delta_amount = MoneyField(
        default = Decimal(0),
        verbose_name=_('delta (amount)'),
        help_text=_('For discount, enter a negative value.'))
    variation = models.ForeignKey(
        'ProductVariation',
        related_name='choices',
        verbose_name=_('product variation'))

    objects = ProductVariationChoiceQuerySet.as_manager()

    class Meta:
        ordering = ['order']
        unique_together = [
            ['name', 'variation']
        ]
        verbose_name = _('product variation choice')
        verbose_name_plural = _('product variation choices')

    def delta(self):
        return self.delta_amount


class ConditionQuerySet(InheritanceQuerySetMixin, models.QuerySet):
    def met(self, person):
        met_pks = []

        for condition in self.select_subclasses():
            if condition.is_met(person):
                met_pks.append(condition.pk)

        return self.filter(pk__in=met_pks)


class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)

    def holdings(self):
        from .models import Holding
        return Holding.objects.filter(products__in=self)

    def events(self):
        return events.models.MainEvent.objects.filter(products__in = self).distinct()


class HoldingQuerySet(models.QuerySet):
    # METHODS RETURNING HOLDING QUERYSETS #

    def purchased(self):
        return self.filter(cart__purchased__isnull=False)

    def unpurchased(self):
        return self.filter(cart__purchased__isnull=True)

    def organized_by(self, organizer):
        return self.filter(product__main_event__organizer = organizer)

    # METHODS RETURNING OTHER QUERYSETS #

    def holders(self):
        return people.models.Person.objects.filter(holdings__in=self).distinct()

    def products(self):
        return products.models.Product.objects.filter(holdings__in=self).distinct()

    # METHODS RETURNING NUMERIC VALUES #

    def total_cost(self):
        return self.annotate(price=models.Sum('product__price')).aggregate(models.Sum('price', field='price*quantity'))['price__sum']\
            or 0

    def quantity(self):
        return self.aggregate(models.Sum('quantity'))['quantity__sum'] or 0


    def purchased_total_cost(self):
        return self.annotate(price=models.Sum('purchase_price')).aggregate(models.Sum('price', field='price*quantity'))['price__sum'] or 0

    def prepare_for_purchase(self, ignore_limits=False, modify_history_allowed=False):
        for i in self:
            i.prepare_for_purchase(
                ignore_limits=ignore_limits,
                modify_history_allowed=modify_history_allowed)

    def charge(self, cart, stripe_token):
        person = cart.person

        stripe_customer = stripe.Customer.create(
            source=stripe_token,
            description=person.get_full_name(),
            email=person.email,
            metadata={'liubiljett_person_id': person.pk}
        )
        completed_charges = []
        try:
            for organizer in self.products().events().organizers():
                charge_amount = self.organized_by(organizer).purchased_total_cost()

                stripe_organizer_person_token = stripe.Token.create(
                    customer=stripe_customer,
                    stripe_account=organizer.stripe_account_id
                )

                charge = stripe.Charge.create(
                    source=stripe_organizer_person_token,
                    amount=int(charge_amount*100),  # Convert price from kr to ore.
                    currency=settings.CURRENCY,
                    stripe_account=organizer.stripe_account_id
                )
                if charge.status == "succeeded":
                    completed_charges.append(charge)
                    Transaction.objects.create(
                        amount=charge_amount,
                        stripe_charge=charge.id,
                        organizer=organizer,
                        cart=cart
                    )
        except stripe.error.CardError as e:
            # The payment to the current organizer has failed.
            # Roll back the database transaction.
            logger.exception("A charge failed.")
            for charge in completed_charges:
                try:
                    stripe.Refund.create(charge=charge.id)
                except stripe.error.StripeError:
                    logger.exception("An error occured while refunding charges.")
            raise e
        finally:
            stripe_customer.delete()

    def email_ticket(self):
        for i in self:
            i.email_ticket()


class CartQuerySet(models.QuerySet):
    def purchased(self):
        return self.filter(purchased__isnull=False)

    def unpurchased(self):
        return self.filter(purchased__isnull=True)

    def holdings(self):
        return products.models.Holding.objects.filter(cart__in=self)
