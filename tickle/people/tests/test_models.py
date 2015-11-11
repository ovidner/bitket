from __future__ import absolute_import, unicode_literals

from datetime import date

from django.test import TestCase

from hamcrest import *

from ..factories import PersonFactory, StudentUnionFactory


class PersonMethodTests(TestCase):
    def test_get_pid(self):
        person = PersonFactory.build()

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(1950, 1, 15), '0001', False)
        assert_that(person.pid, equal_to('19500115-0001'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(1950, 1, 15), '0008', True)
        assert_that(person.pid, equal_to('19500175-0008'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(2001, 1, 15), '0001', False)
        assert_that(person.pid, equal_to('20010115-0001'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(2001, 1, 15), '0008', True)
        assert_that(person.pid, equal_to('20010175-0008'))

        person.birth_date, person.pid_code, person.pid_coordination = (
            date(2001, 1, 15), None, False)
        assert_that(person.pid, equal_to('20010115-0000'))

    def test_set_pid(self):
        person = PersonFactory.build()

        person.pid = '500115-0000'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), None, False)))

        person.pid = '19500115-0000'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), None, False)))

        person.pid = '500115+0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1850, 1, 15), '0001', False)))

        person.pid = '500115-0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), '0001', False)))

        person.pid = '500115-T009'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), 'T009', False)))

        person.pid = '19500115-T009'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), 'T009', False)))

        person.pid = '19500115-0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), '0001', False)))

        person.pid = '19500175-0008'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(1950, 1, 15), '0008', True)))

        person.pid = '20010115-0001'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(2001, 1, 15), '0001', False)))

        person.pid = '20010175-0008'
        assert_that(
            (person.birth_date, person.pid_code, person.pid_coordination),
            equal_to((date(2001, 1, 15), '0008', True)))

    def test_get_full_name(self):
        person = PersonFactory.build(
            first_name='First',
            last_name='Last')
        assert_that(person.get_full_name(), equal_to('First Last'))

    def test_get_short_name(self):
        person = PersonFactory.build(
            first_name='First',
            last_name='Last')
        assert_that(person.get_short_name(), equal_to('First L.'))
