from __future__ import absolute_import, unicode_literals
import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.db import models
from django.db import transaction as db_transaction
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from dry_rest_permissions.generics import allow_staff_or_superuser

from tickle.common.db.fields import MoneyField, NameField, SlugField, DescriptionField
from tickle.common.behaviors import NameMixin, NameSlugMixin, NameSlugDescriptionMixin
from tickle.modifiers.models import HoldingModifier
from tickle.payments.models import Transaction
from tickle.common.models import Model
from tickle.organizers.models import Organizer
from .exceptions import (ConflictingProductVariationChoices, ExceedsLimit,
                         ModifiesHistory)
from .querysets import ProductQuerySet, HoldingQuerySet, CartQuerySet


@python_2_unicode_compatible
class Cart(Model):
    person = models.ForeignKey(
        'people.Person',
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
        self.purchased = now()
        self.save()
        self.holdings.charge(self.person, stripe_token)


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
        #if self._will_exceed_personal_limit():
        #    raise ExceedsLimit(_('Exceeding personal quantity limit.'))
        if self.is_purchased:
            raise ModifiesHistory(
                _('This will change history of purchased objects. Denied.'))

        super(Holding, self).save(force_insert, force_update, using,
                                  update_fields)

    @staticmethod
    def has_create_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.person and not self.is_purchased

    def has_object_destroy_permission(self, request):
        return self.has_object_write_permission(request)

    def _will_modify_purchased_holding(self):
        return self.cart.purchased

    def _will_exceed_personal_limit(self):
        # todo: make this work for other quantities than 1
        return (self.product.holdings.filter(person=self.person).exclude(
            pk=self.pk).quantity() + self.quantity) <= self.product.personal_limit

    def _has_conflicting_product_variation_choices(self):
        if not self.pk:
            return False
        return self.product_variation_choices.values(
            'variation').annotate(count=models.Count('id')).order_by().filter(
            count__gt=1).exists()

    def send_ticket(self):
        msg = TemplatedEmail(
            to=[self.person.pretty_email],
            from_email='Biljett SOF15 <biljett@sof15.se>',
            subject_template='tickle/email/ticket_subject.txt',
            body_template_html='tickle/email/ticket.html',
            context={
                'holding': self,
                'host': settings.PRIMARY_HOST,
            },
            tags=['tickle', 'ticket'])
        msg.send()

    #Discount from product variations
    def product_variation_choice_delta(self):
        delta = Decimal(0)
        for choice in self.product_variation_choices.all():
            delta += choice.delta()

    #The final price of the holding.
    #Should only be used when all ProducVariationChoices have been added properly
    def price(self):
        return self.product.base_price + self.product.modifier_delta(self.person) + self.product_variation_choice_delta()

    #Creates HoldingModifiers for the holding, and sets purchase_price
    def prepare_for_purchase(self):
        temp_price = self.product.base_price

        for product_modifier in self.product.product_modifiers.eligible(self.person):
            holding_modifier = HoldingModifier(product_modifier = product_modifier, holding = self)
            holding_modifier.save()
            temp_price += product_modifier.delta()
        self.purchase_price = temp_price
        self.save()

    @property
    def is_purchased(self):
        return self.cart.purchased is not None

    @property
    def total(self):
        return self.product.price * self.quantity


class Product(NameSlugDescriptionMixin, Model):
    name = NameField()
    slug = SlugField()
    description = DescriptionField()

    main_event = models.ForeignKey(
        'events.MainEvent',
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
        return self.product_modifiers.eligible(person).real_delta()

    #Not used for calculating final price.
    def modified_price(self, person):
        self.base_price + self.product_modifiers.eligible(person).real_delta()

    def has_reached_limit(self):
        return self.limit and self.holdings.purchased().quantity() >= self.limit

    def eligible_product_modifiers(self, person):
        return self.product_modifiers.eligible(person)


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

    class Meta:
        ordering = ['order']
        unique_together = [
            ['name', 'variation']
        ]
        verbose_name = _('product variation choice')
        verbose_name_plural = _('product variation choices')

    def delta(self):
        return self.delta_amount
