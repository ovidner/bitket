from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from hamcrest import *

from ..factories import PersonFactory, StudentUnionFactory


class PersonMethodTests(TestCase):
    def test_get_full_name(self):
        person = PersonFactory(
            first_name='First',
            last_name='Last')
        assert_that(person.get_full_name(), equal_to('First Last'))

    def test_get_short_name(self):
        person = PersonFactory(
            first_name='First',
            last_name='Last')
        assert_that(person.get_short_name(), equal_to('First L.'))
