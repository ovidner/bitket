from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from hamcrest import *

from ..factories import PersonFactory
from ..models import Person


class PersonManagerTests(TestCase):
    def test_create_user(self):
        person = Person.objects.create_user(
            first_name='First name',
            last_name='Last name',
            email='email@domain.com',
            password='Password')
        person = Person.objects.get(pk=person.pk)
        assert_that(person.first_name, equal_to('First name'))
        assert_that(person.last_name, equal_to('Last name'))
        assert_that(person.email, equal_to('email@domain.com'))
        assert_that(person.has_usable_password())

    def test_create_superuser(self):
        person = Person.objects.create_superuser(
            first_name='First name',
            last_name='Last name',
            email='email@domain.com',
            password='Password')
        person = Person.objects.get(pk=person.pk)
        assert_that(person.first_name, equal_to('First name'))
        assert_that(person.last_name, equal_to('Last name'))
        assert_that(person.email, equal_to('email@domain.com'))
        assert_that(person.is_staff)
        assert_that(person.is_superuser)
        assert_that(person.has_usable_password())
