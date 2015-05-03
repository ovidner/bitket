# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import F, Q, Count
from django.utils.translation import ungettext_lazy, ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now, get_current_timezone
from django.core.exceptions import ValidationError
from django.template.defaultfilters import date as format_date
from mptt.models import MPTTModel, TreeForeignKey

from tickle.models import Person, PersonQuerySet, BaseDiscount


class WorkerQuerySet(PersonQuerySet):
    def workers(self):
        return self.filter(models.Q(shift_registrations__isnull=False) | models.Q(functionary__isnull=False)).distinct()

    def functionaries(self):
        return self.filter(functionary__isnull=False)


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

    registered = models.DateTimeField(blank=True, verbose_name=_('registration timestamp'))

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
        try:
            return self.person.full_name
        except models.ObjectDoesNotExist:
            return '<No person set>'
        
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.registered = now()
        
        super(Functionary, self).save(force_insert, force_update, using, update_fields)


@python_2_unicode_compatible
class FunctionaryDiscount(BaseDiscount):
    shifts = models.PositiveIntegerField(verbose_name=_('shifts'),
                                         help_text=_('Number of shifts to work to be eligible for this discount.'))

    class Meta:
        ordering = ('shifts',)
        verbose_name = _('functionary discount')
        verbose_name_plural = _('functionary discounts')

    def __str__(self):
        return '{0} {1}, {2}'.format(self.shifts, _('shift/s'), self.readable_discount())

    def eligible(self, person):
        return hasattr(person, 'functionary') and person.shift_registrations.count() == self.shifts

    def description(self):
        return '{0}, {1}'.format(self._meta.verbose_name, ungettext_lazy("%d shift", "%d shifts") % self.shifts)


@python_2_unicode_compatible
class FunctionaryShiftTypeDiscount(BaseDiscount):
    shift_types = models.ManyToManyField('ShiftType', related_name='shift_type_discounts', verbose_name=_('shift types'))
    text = models.CharField(max_length=256, verbose_name=_('text'))

    class Meta:
        ordering = ('text',)

        verbose_name = _('shift type discount')
        verbose_name_plural = _('shift type discounts')

    def __str__(self):
        return '{0}, {1}'.format(self.text, self.readable_discount())

    def eligible(self, person):
        return person.shift_registrations.filter(shift__shift_type__in=self.shift_types.all()).exists()

    def description(self):
        return self.text


@python_2_unicode_compatible
class ShiftType(MPTTModel):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    parent = TreeForeignKey('self', related_name='children', null=True, blank=True, verbose_name=_('parent'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))

    class Meta:
        ordering = ('name',)

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
    def _exclude_critical_equals_alarming(self):
        return self.exclude(people_critical=F('people_alarming'))

    def _exclude_alarming_equals_max(self):
        return self.exclude(people_alarming=F('people_max'))

    def annotate_registrations_count(self):
        return self.annotate(registrations_count=Count('registrations'))

    def public(self):
        return self.filter(public=True)

    def critical(self):
        return self.annotate_registrations_count().exclude(
            # Well, obviously.
            registrations_count__gt=F('people_critical'),
        ).exclude(
            # These are ok.
            people_max=F('people_critical'),
            registrations_count=F('people_critical'),
        ).distinct()

    def alarming(self):
        return self.annotate_registrations_count().exclude(
            # These can never count as alarming, they're either critical or ok.
            people_critical=F('people_alarming'),
        ).exclude(
            # These can never count as alarming, they're either critical or ok.
            people_max=F('people_alarming'),
        ).exclude(
            registrations_count__lte=F('people_critical'),
        ).exclude(
            registrations_count__gt=F('people_alarming'),
        ).distinct()

    def ok(self):
        return self.annotate_registrations_count().exclude(
            # Overstaffed shifts are not ok.
            registrations_count__gt=F('people_max'),
        ).exclude(
            # Well, obviously.
            registrations_count__lt=F('people_alarming'),
        ).exclude(
            # A shift with alarming=3, max=5 is not ok if registrations=3
            ~Q(people_alarming=F('people_max')),
            registrations_count=F('people_alarming'),
        ).distinct()

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
        ordering = ('shift_type', 'start', 'end')

        verbose_name = _('shift')
        verbose_name_plural = _('shifts')

    def __str__(self):
        return '{0}: {1}'.format(self.shift_type, self.pretty_start_end)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.people_critical <= self.people_alarming:
            raise ValidationError({'people_critical': _('Critical number must be less than or equal to alarming.'),
                                   'people_alarming': _('Critical number must be less than or equal to alarming.')})

        if not self.people_alarming <= self.people_max:
            raise ValidationError({'people_alarming': _('Alarming number must be less than or equal to maximum.'),
                                   'people_max': _('Alarming number must be less than or equal to maximum.')})

        return super(Shift, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                       update_fields=update_fields)

    @property
    def pretty_start_end(self):
        tz = get_current_timezone()
        start = self.start.astimezone(tz)
        end = self.end.astimezone(tz)
        time_format = "H:i"
        date_format = "d b"
        if start.date() == end.date():
            return '{0} {1} – {2}'.format(format_date(start, date_format), format_date(start, time_format),
                                          format_date(end, time_format))
        return '{0} {1} – {2} {3}'.format(format_date(start, date_format), format_date(start, time_format),
                                          format_date(end, date_format), format_date(end, time_format))

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
