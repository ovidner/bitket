# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey

from tickle.models import Person, BaseDiscount


@python_2_unicode_compatible
class Worker(models.Model):
    person = models.OneToOneField('tickle.Person', related_name='worker')

    ice_number = models.CharField(max_length=16, null=True, blank=True, verbose_name=_('ICE number'))

    class Meta:
        verbose_name = _('worker')
        verbose_name_plural = _('workers')

    def __str__(self):
        return self.person.full_name


class WorkerDiscount(BaseDiscount):
    shifts = models.PositiveIntegerField(verbose_name=_('shifts'),
                                         help_text=_('Number of shifts to work to be eligible for this discount.'))

    class Meta:
        verbose_name = _('worker discount')
        verbose_name_plural = _('worker discounts')

    def eligible(self, person):
        return person.shift_registrations.count() == self.shifts


@python_2_unicode_compatible
class ShiftType(MPTTModel):
    name = models.CharField(max_length=256)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True)

    class Meta:
        verbose_name = _('shift type')
        verbose_name_plural = _('shift types')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Location(MPTTModel):
    name = models.CharField(max_length=256)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True)

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Shift(models.Model):
    shift_type = TreeForeignKey('ShiftType', related_name='shifts')

    start = models.DateTimeField()
    end = models.DateTimeField()

    location = models.ForeignKey('Location', related_name='shifts', null=True, blank=True)

    responsible = models.ForeignKey('tickle.Person', related_name='shift_responsibilities', null=True, blank=True)

    people_max = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('maximum number of workers'))
    people_warning = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('warning number of workers'))
    people_critical = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('critical number of workers'), help_text=_('The number of workers needed on this shift for critical operation.'))

    public = models.BooleanField(default=True, verbose_name=_('public'), help_text=_("If unchecked, this shift won't be visible or available for registration by public users."))

    class Meta:
        verbose_name = _('shift')
        verbose_name_plural = _('shifts')

    def __str__(self):
        return u'%s %s – %s' % (self.shift_type.name, self.start, self.end)


@python_2_unicode_compatible
class ShiftRegistration(models.Model):
    shift = models.ForeignKey('Shift', related_name='registrations')
    person = models.ForeignKey('tickle.Person', related_name='shift_registrations')

    class Meta:
        verbose_name = _('shift registration')
        verbose_name_plural = _('shift registrations')

    def __str__(self):
        return u'%s: %s' % (self.person, self.shift)
