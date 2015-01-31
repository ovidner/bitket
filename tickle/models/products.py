# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Event(MPTTModel):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    parent = TreeForeignKey('self', null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name

    @property
    def public_name(self):
        return self._public_name or self.name


@python_2_unicode_compatible
class TicketType(Product):
    product = models.OneToOneField('Product', related_name='ticket_type', parent_link=True, verbose_name=_('product'))
    events = models.ManyToManyField('Event', verbose_name=_('events'))

    def __str__(self):
        return self.product.name


class HoldingQuerySet(models.QuerySet):
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

    def __str__(self):
        return u'{0}, {1}'.format(self.holdings, self.delivered)


@python_2_unicode_compatible
class Purchase(models.Model):
    person = models.ForeignKey('Person', verbose_name=_('person'))
    # holdings = models.ManyToManyField('Holding', null=True, verbose_name=_('holdings'))

    purchased = models.DateTimeField(verbose_name=_('purchased'))

    valid = models.BooleanField(default=True, verbose_name=_('valid'))

    def __str__(self):
        return u'{0}'.format(self.person)