# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey

from tickle.models import Person


@python_2_unicode_compatible
class Worker(models.Model):
    person = models.OneToOneField('tickle.Person', related_name='worker')

    ice_number = models.CharField(max_length=16, verbose_name=_('ICE number'))

    def __str__(self):
        return self.person.full_name


@python_2_unicode_compatible
class ShiftType(MPTTModel):
    name = models.CharField(max_length=256)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True)

    def __str__(self):
        return self.name


class Shift(models.Model):
    shift_type = TreeForeignKey('ShiftType', related_name='shifts')

    start = models.DateTimeField()
    end = models.DateTimeField()

    responsible = models.ForeignKey('tickle.Person', related_name='shift_responsibilities')
    min_workers = models.PositiveIntegerField(default=1, verbose_name=_('minimum number of workers'), help_text=_('The number of workers needed on this shift for critical operation.'))
    max_workers = models.PositiveIntegerField(verbose_name=_('maximum number of workers'))
    public = models.BooleanField(default=True, verbose_name=_('public'), help_text=_("If unchecked, this shift won't be visible or available for registration by public users."))


class ShiftRegistration(models.Model):
    shift = models.ForeignKey('Shift')
    worker = models.ForeignKey('Worker')