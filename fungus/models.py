# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from mptt.models import MPTTModel, TreeForeignKey

from tickle.models import Person


@python_2_unicode_compatible
class Worker(models.Model):
    person = models.OneToOneField('tickle.Person', related_name='worker')

    ice_number = models.CharField(max_length=16, null=True, blank=True, verbose_name=_('ICE number'))

    def __str__(self):
        return self.person.full_name


@python_2_unicode_compatible
class ShiftType(MPTTModel):
    name = models.CharField(max_length=256)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Location(MPTTModel):
    name = models.CharField(max_length=256)
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True)

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

    def __str__(self):
        return u'%s %s – %s' % (self.shift_type.name, self.start, self.end)


@python_2_unicode_compatible
class ShiftRegistration(models.Model):
    shift = models.ForeignKey('Shift', related_name='registrations')
    person = models.ForeignKey('tickle.Person', related_name='shift_registrations')

    def __str__(self):
        return u'%s: %s' % (self.person, self.shift)