# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings


@python_2_unicode_compatible
class Person(models.Model):
    first_name = models.CharField(max_length=256, verbose_name=_('first name'))
    last_name = models.CharField(max_length=256, verbose_name=_('last name'))

    id_number = models.CharField(max_length=11, unique=True, verbose_name=_('national identification number'))
    liu_id = models.OneToOneField('liu.LiUID', blank=True, null=True, verbose_name=_('LiU ID'))

    phone = models.CharField(max_length=24, blank=True, verbose_name=('phone number'))
    email = models.EmailField(max_length=256, unique=True, verbose_name=_('email address'))

    special_nutrition = models.ManyToManyField('SpecialNutrition', null=True, blank=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if hasattr(self, 'user') and not hasattr(self, 'liu_id'):
            # Set username to email, only if a LiU id doesn't exist.
            self.user.username = self.email
            self.user.save()

        super(Person, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


@python_2_unicode_compatible
class SpecialNutrition(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TickleUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have a username')

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
    person = models.OneToOneField('Person', related_name='user', null=True, blank=True)

    username = models.CharField(max_length=256, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = TickleUserManager()

    USERNAME_FIELD = 'username'

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
