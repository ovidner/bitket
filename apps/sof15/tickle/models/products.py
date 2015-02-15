# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


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
    description = models.TextField(blank=True, verbose_name=_('description'))

    price = models.PositiveIntegerField(verbose_name=_('price'))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TicketType(Product):
    event = models.ForeignKey('Event', verbose_name=_('event'))

    def __str__(self):
        return u'{0}, {1}'.format(self.event, self.name)


@python_2_unicode_compatible
class Holding(models.Model):
    person = models.ForeignKey('Person')
    product = models.ForeignKey('Product')

    # todo: add amount

    def __str__(self):
        return '{0} {1}'.format(self.product, self.person)


@python_2_unicode_compatible
class Delivery(models.Model):
    holdings = models.ManyToManyField('Holding')
    delivered = models.DateTimeField()

    def __str__(self):
        return '{0}, {1}'.format(self.holding, self.delivered)


@python_2_unicode_compatible
class Purchase(models.Model):
    person = models.ForeignKey('Person')
    holdings = models.ManyToManyField('Holding')

    purchased = models.DateTimeField()

    def __str__(self):
        return '{0}'.format(self.person)