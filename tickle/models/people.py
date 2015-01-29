# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from guardian.shortcuts import assign_perm


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
    liu_id = models.OneToOneField('liu.LiUID', blank=True, null=True, verbose_name=_('LiU ID'))

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
            if not self.user.password:
                self.user.set_password(self.generate_user_password())
            self.user.save()

            # Everybody must be able to show their own profiles. This way we don't have to write special checks in
            # the views.
            assign_perm('view_person', self.user, self)

        super(Person, self).save(*args, **kwargs)

    def clean_pid_code(self):
        # If pid_code == '' then we should actually save NULL for uniqueness check, see above.
        return self.cleaned_data['pid_code'] or None

    @property
    def pid(self):
        if self.birth_date:
            return '{0:0>2}{1:0>2}{2:0>2}-{3}'.format(
                str(self.birth_date.year)[-2:],
                self.birth_date.month,
                self.birth_date.day,
                self.pid_code or '0000'
            )
        else:
            return None

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def generate_user_password(self):
        password = TickleUser.objects.make_random_password()

        template_data = {
            'person': self,
            'password': password,
            'url': settings.URL
        }
        subject = 'Användarkonto hos SOF'
        html_body = render_to_string('tickle/email/tickle_user_account_created.html', template_data)

        msg = EmailMultiAlternatives(subject=subject, from_email=settings.SUPPORT_EMAIL, to=[self.email])
        msg.attach_alternative(html_body, "text/html")
        msg.send()

        return password


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
        "Is the user a member of staff?"
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
