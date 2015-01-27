# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=256)

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

    categories = models.ManyToManyField('Category', null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('price'))
    quantitative = models.BooleanField(default=False,
                                       help_text=_('Can you purchase more than one (1) of this product?'))

    def __str__(self):
        return self.name

    @property
    def public_name(self):
        return self._public_name or self.name


@python_2_unicode_compatible
class TicketType(Product):
    product = models.OneToOneField('Product', related_name='ticket_type', parent_link=True)
    events = models.ManyToManyField('Event', verbose_name=_('events'))

    def __str__(self):
        return self.product.name


class HoldingQuerySet(models.QuerySet):
    def tickets(self):
        return self.filter(product__ticket_type__isnull=False)


@python_2_unicode_compatible
class Holding(models.Model):
    person = models.ForeignKey('Person', related_name='holdings')
    product = models.ForeignKey('Product', related_name='holdings')

    quantity = models.PositiveIntegerField(default=1)  # todo: validate this! base on Product.quantitative

    objects = HoldingQuerySet.as_manager()

    def __str__(self):
        return u'{0} {1}'.format(self.product, self.person)

    @property
    def total(self):
        return self.product.price * self.quantity


@python_2_unicode_compatible
class Delivery(models.Model):
    holdings = models.ManyToManyField('Holding')
    delivered = models.DateTimeField()

    def __str__(self):
        return u'{0}, {1}'.format(self.holdings, self.delivered)


@python_2_unicode_compatible
class Purchase(models.Model):
    person = models.ForeignKey('Person')
    holdings = models.ManyToManyField('Holding', null=True)

    purchased = models.DateTimeField()

    valid = models.BooleanField(default=True)

    def __str__(self):
        return u'{0}'.format(self.person)