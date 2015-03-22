# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.backends import ModelBackend
from django.db.transaction import atomic

from django_auth_ldap.backend import LDAPBackend

from tickle.models import TickleUser, Person
from tickle.auth.settings import LiUStudentLDAPSettings, LiUEmployeeLDAPSettings

import logging
logger = logging.getLogger(__name__)


class _LiUBaseLDAPBackend(LDAPBackend):
    """
    DON'T USE THIS AS YOUR AUTH BACKEND! Use the LiUStudentBackend and/or LiUEmployeeBackend instead.
    """

    def _get_settings(self):
        """
        Overridden since the _settings are always set in our subclasses.
        """

        return self._settings

    def _populate_person_data(self, person, ldap_user):
        """
        Feel free to override this in your subclass. You don't have to save the person object, we'll do it later.
        """
        person.first_name = ldap_user.attrs['givenName'][0]
        person.last_name = ldap_user.attrs['sn'][0]

    def _get_or_create_person(self, user, ldap_user):
        if user.person:
            # Well then, we're done.
            return user.person, False

        liu_id = ldap_user.attrs['cn'][0]
        email = ldap_user.attrs['mail'][0]

        person, created = Person.objects.get_or_create(liu_id=liu_id, defaults={'email': email})

        return person, created

    def get_or_create_user(self, username, ldap_user):
        # Something funny *might* happen on the way, let's make sure we never end up with an inconsistent db state
        with atomic():
            user, user_created = super(_LiUBaseLDAPBackend, self).get_or_create_user(username, ldap_user)

            person, person_created = self._get_or_create_person(user, ldap_user)

            # Runs any subclass specific logic for populating the Person object with extra data.
            self._populate_person_data(person, ldap_user)

            person.save()

            if not user.person:
                user.person = person
                user.save()

            return user, user_created


class LiUStudentLDAPBackend(_LiUBaseLDAPBackend):
    """
    An authentication backend for LiU students.
    """

    settings_prefix = 'LIU_STUDENT_LDAP_'
    _settings = LiUStudentLDAPSettings(settings_prefix)

    def _populate_person_data(self, person, ldap_user):
        super(LiUStudentLDAPBackend, self)._populate_person_data(person, ldap_user)

        person.fill_kobra_data(save=False, overwrite_name=False)


class LiUEmployeeLDAPBackend(_LiUBaseLDAPBackend):
    """
    An authentication backend for LiU employees.
    """

    settings_prefix = 'LIU_EMPLOYEE_LDAP_'
    _settings = LiUEmployeeLDAPSettings(settings_prefix)


class TickleBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        """
        Authenticates users against their email address.
        """
        try:
            user = TickleUser.objects.get(person__email__exact=username)
            if user.check_password(password):
                return user

        except TickleUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            TickleUser().set_password(password)
