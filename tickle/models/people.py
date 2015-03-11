# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from liu.kobra import KOBRAClient

from tickle.utils.mail import TemplatedEmail
from tickle.fields import SEPersonalIdentityNumberField


@python_2_unicode_compatible
class StudentUnion(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    def __str__(self):
        return self.name


class LiUIDQuerySet(models.QuerySet):
    def fetch(self):
        for i in self:
            i.fetch()


@python_2_unicode_compatible
class LiUID(models.Model):
    """
    Stores a LiU ID. Fetches information from KOBRA with the fetch() method.

    liu_id is the only mandatory field.
    """
    liu_id = models.CharField(max_length=10, verbose_name=_('LiU ID'))

    first_name = models.CharField(max_length=256, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=256, blank=True, verbose_name=_('last name'))

    pid = models.CharField(max_length=11, blank=True, verbose_name=_('national identity number'))

    barcode_number = models.CharField(max_length=32, blank=True, verbose_name=_('magnet/barcode card number'))
    rfid_number = models.CharField(max_length=32, blank=True, verbose_name=_('RFID card number'))

    student_union = models.ForeignKey('StudentUnion', related_name='members', blank=True, null=True,
                                      verbose_name=_('student union'))

    blocked = models.NullBooleanField(verbose_name=_('blocked'))

    objects = LiUIDQuerySet.as_manager()

    class Meta:
        verbose_name = _('LiU ID')
        verbose_name_plural = _('LiU IDs')

    def __str__(self):
        return self.liu_id

    def fetch(self):
        """
        Updates the fields using KOBRA. Uses LiU ID to find user.
        """
        client = KOBRAClient(settings.LIU_KOBRA_USER, settings.LIU_KOBRA_API_KEY)
        # We don't catch any exceptions here. You might want to catch them in your own applications instead.
        data = client.get_student(liu_id=self.liu_id)

        if data:
            self.first_name = data['first_name']
            self.last_name = data['last_name']

            self.id_number = data['personal_number']

            self.barcode_number = data['barcode_number']
            self.rfid_number = data['rfid_number']

            self.student_union = StudentUnion.objects.get_or_create(name=data['union'])[0]

            self.blocked = data['blocked']

            self.save()


@python_2_unicode_compatible
class Person(models.Model):
    first_name = models.CharField(max_length=256, verbose_name=_('first name'))
    last_name = models.CharField(max_length=256, verbose_name=_('last name'))

    birth_date = models.DateField(null=True, blank=True)
    pid_code = models.CharField(
        max_length=4,
        null=True,  # This is needed for the uniqueness check. (NULL != NULL but '' == '')
        blank=True,
        verbose_name=_('national identity code'),
        help_text=_('Last 4 digits in Swedish national identity number.'),
    )
    liu_id = models.OneToOneField('LiUID', blank=True, null=True, verbose_name=_('LiU ID'))

    phone = models.CharField(max_length=24, blank=True, verbose_name=('phone number'))
    email = models.EmailField(max_length=256, unique=True, verbose_name=_('email address'))

    special_nutrition = models.ManyToManyField(
        'SpecialNutrition',
        null=True,
        blank=True,
        verbose_name=_('special nutrition'),
        help_text=_('Specify any special nutritional needs or habits.')
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_('other information'),
        help_text=_('Want us to know something else?')
    )
    our_notes = models.TextField(
        blank=True,
        verbose_name=_('our notes'),
        help_text=_('Internal notes. Cannot be seen by this person.')
    )

    class Meta:
        unique_together = (
            # If both are specified, the combination must be unique. Two birth dates with NULL as pid_code should pass
            # as we want it to.
            ('birth_date', 'pid_code'),
        )

        ordering = ('first_name', 'last_name')

        permissions = (
            ('view_person', _('Can view person')),
        )

        verbose_name = _('person')
        verbose_name_plural = _('people')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if hasattr(self, 'user'):
            # Set username to email, only if a LiU id doesn't exist.
            if not self.liu_id:
                self.user.username = self.email
            else:
                self.user.username = self.liu_id

            self.user.save()

        super(Person, self).save(*args, **kwargs)

    def clean_pid_code(self):
        # If pid_code == '' then we should actually save NULL for uniqueness check, see above.
        return self.cleaned_data['pid_code'] or None

    def _get_pid(self):
        if self.birth_date:
            return '{0:0>2}{1:0>2}{2:0>2}-{3}'.format(
                str(self.birth_date.year)[-2:],
                self.birth_date.month,
                self.birth_date.day,
                self.pid_code or '0000',
            )
        else:
            return None

    def _set_pid(self, value):
        self.birth_date, self.pid_code = SEPersonalIdentityNumberField().clean(value)

    pid = property(_get_pid, _set_pid)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def pretty_email(self):
        return '{0} <{1}>'.format(self.full_name, self.email)


@python_2_unicode_compatible
class SpecialNutrition(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    class Meta:
        ordering = ['name']

        verbose_name = _('special nutrition')
        verbose_name_plural = _('special nutritions')

    def __str__(self):
        return self.name


class TickleUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class TickleUser(AbstractBaseUser, PermissionsMixin):
    person = models.OneToOneField('Person', related_name='user', null=True, blank=True, verbose_name=_('person'))

    username = models.CharField(max_length=256, unique=True, verbose_name=_('LiU-ID or email address'))

    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))

    objects = TickleUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_full_name()

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        if self.person:
            return self.person.full_name
        else:
            return self.username

    def get_short_name(self):
        if self.person:
            return self.person.full_name
        else:
            return self.username

    def generate_and_send_password(self):
        password = TickleUser.objects.make_random_password()

        self.set_password(password)

        msg = TemplatedEmail(
            subject='Användarkonto hos SOF',
            to=[self.person.pretty_email],
            body_template_html='tickle/email/tickle_user_account_created.html',
            context={
                'person': self.person,
                'password': password,
                'host': settings.PRIMARY_HOST,
            })
        msg.send()

        return password
