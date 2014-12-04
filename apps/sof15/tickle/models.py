# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey


@python_2_unicode_compatible
class SpecialNutrition(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Person(models.Model):
    first_name = models.CharField(max_length=256, verbose_name=_('first name'))
    last_name = models.CharField(max_length=256, verbose_name=_('last name'))

    id_number = models.CharField(max_length=11, unique=True, verbose_name=_('national identification number'))
    liu_id = models.OneToOneField('liu.LiUID', blank=True, null=True, verbose_name=_('LiU ID'))

    phone = models.CharField(max_length=32, verbose_name=_('mobile number'))
    address_row_1 = models.CharField(max_length=128)
    address_row_2 = models.CharField(max_length=128, null=True, blank=True)
    postal_code = models.CharField(max_length=8)
    city = models.CharField(max_length=64)

    special_nutrition = models.ManyToManyField('SpecialNutrition')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name=_('user account'))

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


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