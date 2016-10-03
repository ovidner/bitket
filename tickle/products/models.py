from __future__ import absolute_import, unicode_literals
import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.utils import IntegrityError

from dry_rest_permissions.generics import allow_staff_or_superuser
from templated_email import send_templated_mail

from ..common import exceptions
from ..common.db.fields import MoneyField, NameField, SlugField, DescriptionField
from ..common.behaviors import NameMixin, NameSlugMixin, NameSlugDescriptionMixin
from ..common.models import Model
from ..organizers.models import Organizer
from ..payments.models import Transaction
from .exceptions import ConflictingProductVariationChoices, ExceedsLimit
from .querysets import ProductQuerySet, HoldingQuerySet, CartQuerySet


@python_2_unicode_compatible
class Cart(Model):
    person = models.ForeignKey(
        'people.Person',
        related_name='carts',
        verbose_name=_('person'))
    main_event = models.ForeignKey(
        'events.MainEvent',
        related_name='carts',
        verbose_name=_('main event'))
    purchased = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('purchased'))

    modifiers = models.ManyToManyField(
        'modifiers.Modifier',
        related_name='carts',
        blank=True,
        verbose_name=_('modifiers'))

    objects = CartQuerySet.as_manager()

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return '{}'.format(self.person)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.modifiers and not self.purchased:
            raise IntegrityError

        super(Cart, self).save(force_insert, force_update, using, update_fields)

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return request.user == self.person

    def has_object_purchase_permission(self, request):
        return request.user == self.person and not self.purchased

    def purchase(self, stripe_token):
        def charge(self, cart, stripe_token):
            person = cart.person

            stripe_customer = stripe.Customer.create(
                source=stripe_token,
                description=person.get_full_name(),
                email=person.email,
                metadata={'liubiljett_person_id': person.pk}
            )
            try:
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

        self.holdings.prepare_for_purchase()
        # This is ugly. fixme!
        if self.person.holdings.quantity() > 1:
            raise exceptions.EventProductLimitExceeded()
        self.purchased = now()
        self.save()
        charge()
        self.holdings.email_ticket()


@python_2_unicode_compatible
class Holding(Model):
    person = models.ForeignKey(
        'people.Person',
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

    def is_purchasable(self, ignore_limits=False, modify_history_allowed=False):
        if not ignore_limits and self._will_exceed_total_limit():
            raise exceptions.TotalProductLimitExceeded()
        if not ignore_limits and self._will_exceed_personal_limit():
            raise exceptions.PersonalProductLimitExceeded()
        if not modify_history_allowed and self.is_purchased:
            raise exceptions.ModifiesHistory()

        return True

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
        'events.MainEvent',
        related_name='products',
        verbose_name=_('main event'))

    price = MoneyField(
        verbose_name=_('price'))
    modifiers = models.ManyToManyField(
        'modifiers.Modifier',
        related_name='products',
        verbose_name=_('modifiers'))

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
