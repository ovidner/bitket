# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Sum
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey
from decimal import Decimal


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Event(MPTTModel):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    parent = TreeForeignKey('self', null=True, blank=True)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)

    def ticket_types(self):
        return self.filter(ticket_type__isnull=False)


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    _public_name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('public name'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    categories = models.ManyToManyField('Category', null=True, blank=True, verbose_name=_('categories'))

    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('price'))
    quantitative = models.BooleanField(default=False,
                                       verbose_name=_('quantitative'),
                                       help_text=_('Can you purchase more than one (1) of this product?'))

    published = models.BooleanField(default=True, verbose_name=_('published'))

    class Meta:
        ordering = ('name',)

        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name

    @property
    def public_name(self):
        return self._public_name or self.name

    def discounted_price(self, person):
        total_discount = Decimal(0)
        for d in self.discounts.all():
            total_discount += d.discount(self.price, person)

        return self.price - total_discount


@python_2_unicode_compatible
class ProductDiscount(models.Model):
    product = models.ForeignKey('Product', related_name='discounts')

    discount_content_type = models.ForeignKey(ContentType)
    discount_object_id = models.PositiveIntegerField()
    discount_object = GenericForeignKey('discount_content_type', 'discount_object_id')

    class Meta:
        verbose_name = _('product discount')
        verbose_name_plural = _('product discounts')

    def __str__(self):
        return self.discount_object.name

    def eligible(self, person):
        return self.discount_object.eligible(person)

    def discount(self, full_price, person):
        if self.eligible(person):
            return self.discount_object.discount(full_price, person)
        return Decimal(0)


@python_2_unicode_compatible
class TicketType(Product):
    product = models.OneToOneField('Product', related_name='ticket_type', parent_link=True, verbose_name=_('product'))
    events = models.ManyToManyField('Event', verbose_name=_('events'))

    class Meta:
        verbose_name = _('ticket type')
        verbose_name_plural = _('ticket types')

    def __str__(self):
        return self.product.name


class HoldingQuerySet(models.QuerySet):
    def quantity(self):
        return self.aggregate(Sum('quantity'))['quantity__sum'] or 0

    def tickets(self):
        return self.filter(product__ticket_type__isnull=False)


@python_2_unicode_compatible
class Holding(models.Model):
    person = models.ForeignKey('Person', related_name='holdings', verbose_name=_('person'))
    product = models.ForeignKey('Product', related_name='holdings', verbose_name=_('product'))

    purchase = models.ForeignKey('Purchase', related_name='holdings', null=True, blank=True, verbose_name=_('purchase'))

    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))

    objects = HoldingQuerySet.as_manager()

    class Meta:
        verbose_name = _('holding')
        verbose_name_plural = _('holdings')

    def __str__(self):
        return u'{0} {1}'.format(self.product, self.person)

    def clean(self):
        if not self.product.quantitative and not self.quantity == 1:
            raise ValidationError(_('Quantity must be exactly 1 for un-quantitative products.'))

    @property
    def total(self):
        return self.product.price * self.quantity


@python_2_unicode_compatible
class Delivery(models.Model):
    holdings = models.ManyToManyField('Holding', verbose_name=_('holdings'))
    delivered = models.DateTimeField(verbose_name=_('delivered'))

    class Meta:
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')

    def __str__(self):
        return u'{0}, {1}'.format(self.holdings, self.delivered)


class PurchaseQuerySet(models.QuerySet):
    def holdings(self):
        return Holding.objects.filter(purchase__in=self)


@python_2_unicode_compatible
class Purchase(models.Model):
    person = models.ForeignKey('Person', verbose_name=_('person'))
    # holdings = models.ManyToManyField('Holding', null=True, verbose_name=_('holdings'))

    purchased = models.DateTimeField(verbose_name=_('purchased'))

    valid = models.BooleanField(default=True, verbose_name=_('valid'))

    objects = PurchaseQuerySet.as_manager()

    class Meta:
        verbose_name = _('purchase')
        verbose_name_plural = _('purchases')

    def __str__(self):
        return u'{0}'.format(self.person)


@python_2_unicode_compatible
class BaseDiscount(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    discount_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True,
                                          verbose_name=_('amount'))
    discount_percent = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                           verbose_name=_('percent'))

    class Meta:
        abstract = True

        verbose_name = _('base discount')
        verbose_name_plural = _('base discounts')

    def __str__(self):
        return self.name

    def calc_percent_discount(self, full_price):
        if self.discount_percent:
            return Decimal(full_price * self.discount_percent).quantize(Decimal('.01'))
        return Decimal(0)

    def eligible(self, person):
        """
        Method checking if the supplied person is eligible for this discount. Subclass this in your discount class and
        make it return True or False.
        """
        return None

    def discount(self, full_price, person):
        if self.eligible(person):
            return self.discount_amount or self.calc_percent_discount(full_price)
        else:
            return Decimal(0)


class StudentUnionDiscount(BaseDiscount):
    student_union = models.ForeignKey('StudentUnion', related_name='discounts', verbose_name=_('student union'))

    class Meta:
        verbose_name = _('student union discount')
        verbose_name_plural = _('student union discounts')

    def eligible(self, person):
        return self.student_union.members.filter(liu_id=person.liu_id).exists()
