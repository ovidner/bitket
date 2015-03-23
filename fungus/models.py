# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import F, Q, Count
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

from tickle.models import Person, PersonQuerySet, BaseDiscount


class WorkerQuerySet(PersonQuerySet):
    def workers(self):
        return self.filter(models.Q(shift_registrations__isnull=False) | models.Q(functionary__isnull=False)).distinct()


class Worker(Person):
    """
    Proxy class to tickle.Person so we can add some Fungus specific methods.
    """
    objects = WorkerQuerySet.as_manager()

    class Meta:
        proxy = True

        verbose_name = _('worker')
        verbose_name_plural = _('workers')


@python_2_unicode_compatible
class Functionary(models.Model):
    person = models.OneToOneField('tickle.Person', related_name='functionary', verbose_name=_('person'))

    registered = models.DateTimeField(auto_now_add=True, verbose_name=_('registration timestamp'))

    ice_number = models.CharField(max_length=16, null=True, blank=True, verbose_name=_('ICE number'))
    b_driving_license = models.BooleanField(default=False, verbose_name=_('B driving license'), help_text=_('Mandatory for driving missions.'))

    signed_contract = models.BooleanField(default=False, verbose_name=_('signed contract'))
    attended_info_meeting = models.BooleanField(default=False, verbose_name=_('attended info meeting'))
    pledge_payed = models.DateTimeField(null=True, blank=True, verbose_name=_('pledge payed'))
    pledge_returned = models.DateTimeField(null=True, blank=True, verbose_name=_('pledge returned'))

    class Meta:
        verbose_name = _('functionary')
        verbose_name_plural = _('functionaries')

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
    name = models.CharField(max_length=256, verbose_name=_('name'))
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, verbose_name=_('parent'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('shift type')
        verbose_name_plural = _('shift types')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Location(MPTTModel):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, verbose_name=_('parent'))

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __str__(self):
        return self.name


class ShiftQuerySet(models.QuerySet):
    def annotate_registrations_count(self):
        return self.annotate(registrations_count=Count('registrations'))

    def public(self):
        return self.filter(public=True)

    def critical(self):
        return self.annotate_registrations_count().exclude(registrations_count__gt=F('people_critical')).distinct()

    def alarming(self):
        return self.annotate_registrations_count().exclude(registrations_count__lte=F('people_critical'), registrations__gt=F('people_alarming')).distinct()

    def ok(self):
        return self.annotate_registrations_count().exclude(registrations_count__lte=F('people_alarming'), registrations__gt=F('people_max')).distinct()

    def overstaffed(self):
        return self.annotate_registrations_count().filter(registrations_count__gt=F('people_max')).distinct()

    def registerable(self):
        return self.public().annotate_registrations_count().filter(registrations_count__lt=F('people_max')).distinct()


@python_2_unicode_compatible
class Shift(models.Model):
    shift_type = TreeForeignKey('ShiftType', related_name='shifts', verbose_name=_('shift type'))

    start = models.DateTimeField(verbose_name=_('start'))
    end = models.DateTimeField(verbose_name=_('end'))

    location = models.ForeignKey('Location', related_name='shifts', null=True, blank=True, verbose_name=_('location'))

    responsible = models.ForeignKey('tickle.Person', related_name='shift_responsibilities', null=True, blank=True, verbose_name=_('responsible'))

    people_max = models.PositiveIntegerField(default=2, verbose_name=_('maximum number of workers'),
                                             help_text=_("The maximum number of workers on this shift. This shift's status will be reported as overstaffed if the number of workers are over this value."))
    people_alarming = models.PositiveIntegerField(default=1, verbose_name=_('alarming number of workers'),
                                                  help_text=_("The number of workers where the system will report the status as alarming."))
    people_critical = models.PositiveIntegerField(default=0, verbose_name=_('critical number of workers'),
                                                  help_text=_("The number of workers where the system will report the status as critical."))

    public = models.BooleanField(default=True, verbose_name=_('public'), help_text=_(
        "If unchecked, this shift won't be visible or available for registration by public users."))

    objects = ShiftQuerySet.as_manager()

    class Meta:
        verbose_name = _('shift')
        verbose_name_plural = _('shifts')

    def __str__(self):
        time_format = "%H:%M"
        date_format = " %A %d %B"
        if self.start.date() == self.end.date():
            return u'%s, %s–%s %s' % (self.shift_type.name, self.start.strftime(time_format), self.end.strftime(time_format), self.start.strftime(date_format))
        return u'%s, %s – %s' % (self.shift_type.name, self.start.strftime(time_format + date_format), self.end.strftime(time_format + date_format))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.people_critical <= self.people_alarming:
            raise ValidationError({'people_critical': _('Critical number must be less than or equal to alarming.'),
                                   'people_alarming': _('Critical number must be less than or equal to alarming.')})

        if not self.people_alarming <= self.people_max:
            raise ValidationError({'people_alarming': _('Alarming number must be less than or equal to maximum.'),
                                   'people_max': _('Alarming number must be less than or equal to maximum.')})
        
        return super(Shift, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    @property
    def status(self):
        people_count = self.registrations.count()

        if people_count <= self.people_critical:
            return 'critical'
        elif people_count <= self.people_alarming:
            return 'alarming'
        elif people_count > self.people_max:
            return 'overstaffed'
        else:
            return 'ok'


@python_2_unicode_compatible
class ShiftRegistration(models.Model):
    shift = models.ForeignKey('Shift', related_name='registrations', verbose_name=_('shift'))
    person = models.ForeignKey('tickle.Person', related_name='shift_registrations', verbose_name=_('person'))

    checked_in = models.DateTimeField(null=True, blank=True, verbose_name=_('checked in'))
    checked_out = models.DateTimeField(null=True, blank=True, verbose_name=_('checked out'))

    class Meta:
        verbose_name = _('shift registration')
        verbose_name_plural = _('shift registrations')

    def __str__(self):
        return u'%s: %s' % (self.person, self.shift)

    @property
    def start(self):
        return self.shift.start
