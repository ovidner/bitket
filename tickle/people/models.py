from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tickle.common.behaviors import NameSlugMixin
from tickle.common.db.fields import (NameField, SlugField, PasswordField,
                                     NullCharField)
from tickle.common.fields import PidField
from tickle.common.models import TickleModel
from tickle.common.utils.email import generate_pretty_email
from tickle.common.utils.kobra import (KobraClient, StudentNotFound,
                                       Unauthorized)
from tickle.conditions.models import Condition


class PidMixin(models.Model):
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('birth date'))
    pid_code = NullCharField(
        max_length=4,
        verbose_name=_('national identity code'),
        help_text=_('Last 4 digits in Swedish national identity number.'))
    pid_coordination = models.BooleanField(
        default=False,
        verbose_name=_('coordination number'),
        help_text=_('Designates if national identity number is a '
                    '<em>samordningsnummer</em>.'))

    class Meta:
        abstract = True

    def _get_pid(self):
        if self.birth_date:
            day = self.birth_date.day

            if self.pid_coordination:
                day += 60

            return '{0:0>4}{1:0>2}{2:0>2}-{3}'.format(
                self.birth_date.year,
                self.birth_date.month,
                day,
                self.pid_code or '0000',
            )
        else:
            return None

    def _set_pid(self, value):
        self.birth_date, self.pid_code, self.pid_coordination = PidField().clean(value)

    pid = property(_get_pid, _set_pid)


class PasswordFieldMixin(object):
    """
    Placed in a mixin since we can't override a Django field.
    """
    password = PasswordField()


class PersonQuerySet(models.QuerySet):
    def fill_kobra_data(self):
        for i in self:
            i.fill_kobra_data(save=True, overwrite_name=False, fail_silently=True)

    def pretty_emails_string(self):
        """
        Returns a string with pretty formatted emails, separated by semicolons
        """

        recipient_list = ''
        values = self.values('first_name', 'last_name', 'email')

        for i in values:
            recipient_list += generate_pretty_email(i['first_name'], i['last_name'], i['email'])

        return recipient_list


class PersonManager(models.Manager.from_queryset(PersonQuerySet),
                    BaseUserManager):
    def create_user(self, first_name, last_name, email, password):
        """
        Creates and saves a User with the given email and password.
        """
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name, last_name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class Person(PidMixin, PasswordFieldMixin, AbstractBaseUser, PermissionsMixin,
             TickleModel):
    first_name = NameField(
        verbose_name=_('first name'))
    last_name = NameField(
        verbose_name=_('last name'))

    liu_id = NullCharField(
        max_length=8,
        unique=True,
        verbose_name=_('LiU ID'))
    liu_card_rfid = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_('LiU card number'))
    liu_student_union = models.ForeignKey(
        'StudentUnion',
        related_name='members',
        null=True,
        blank=True,
        verbose_name=_('student union'))

    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name=_('email address'))

    special_nutrition = models.ManyToManyField(
        'SpecialNutrition',
        blank=True,
        verbose_name=_('special nutrition'),
        help_text=_('Specify any special nutritional needs or habits.'))

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is active'))
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is staff'))

    objects = PersonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        unique_together = [
            # If both are specified, the combination must be unique. Two birth
            # dates with NULL as pid_code should pass as we want it to.
            ['birth_date', 'pid_code', 'pid_coordination']
        ]
        ordering = ['first_name', 'last_name']

        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return '{} {}.'.format(self.first_name, self.last_name[0])

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            password = make_password(None)
        return password

    def met_conditions(self):
        cache_key = 'people.person.{}.met_conditions'.format(self.pk)
        conditions = cache.get(cache_key)
        if conditions is None:
            conditions = Condition.objects.met(person=self)
            cache.set(cache_key, conditions,
                      timeout=settings.CACHE_PERSON_CONDITIONS_TIMEOUT)
        return conditions

    def get_kobra_data(self, fail_silently=False):
        """
        Searches the KOBRA database by the person's attributes in the following
        order:

            1. LiU ID
            2. PID
            3. RFID card number

        Returns a dictionary.
        """

        request = dict()
        if self.liu_id:
            request = {'liu_id': self.liu_id}
        elif self.birth_date and self.pid_code:
            request = {'personal_number': self.pid}
        elif self.liu_card_rfid:
            request = {'rfid_number': self.liu_card_rfid}
        else:
            if fail_silently:
                return
            else:
                raise KeyError('Person object must have LiU id, PID or RFID '
                               'card number defined.')

        data = KobraClient().get_student(**request)

        return data

    def fill_kobra_data(self, save=False, overwrite_name=False, fail_silently=False):
        try:
            data = self.get_kobra_data(fail_silently=fail_silently)
        except (Unauthorized, StudentNotFound) as e:
            if fail_silently:
                return
            raise e

        if data:
            # Now we trust KOBRA to always give us all values. Let's hope it works that way.

            if not self.first_name or overwrite_name:
                self.first_name = data['first_name']
            if not self.last_name or overwrite_name:
                self.last_name = data['last_name']

            # We always overwrite these.
            self.pid = data['personal_number']
            self.liu_id = data['liu_id']
            self.liu_card_rfid = data['rfid_number'] or ''  # Some people actually have no LiU card

            if data['union']:
                self.liu_student_union = StudentUnion.objects.get_or_create(name=data['union'])[0]

            if save:
                self.save()

        return self

    @property
    def pretty_email(self):
        return generate_pretty_email(self.first_name, self.last_name, self.email)


@python_2_unicode_compatible
class SpecialNutrition(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    class Meta:
        ordering = ['name']

        verbose_name = _('special nutrition')
        verbose_name_plural = _('special nutritions')

    def __str__(self):
        return self.name


class StudentUnion(models.Model):
    name = NameField(unique=True)
    slug = SlugField(unique=True)

    class Meta:
        verbose_name = _('student union')
        verbose_name_plural = _('student unions')
