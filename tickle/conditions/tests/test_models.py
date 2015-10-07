from __future__ import absolute_import, unicode_literals

from hamcrest import *

from django.test import TestCase

from tickle.people.factories import PersonFactory, StudentUnionFactory
from ..factories import ConditionFactory, StudentUnionMemberConditionFactory


class ConditionMethodTests(TestCase):
    def test_is_met(self):
        condition = ConditionFactory()
        assert_that(calling(condition.is_met), raises(Exception))


class StudentUnionMemberConditionTests(TestCase):
    def test_is_met(self):
        student_union = StudentUnionFactory()
        condition = StudentUnionMemberConditionFactory(
            student_union=student_union)
        person = PersonFactory(
            liu_student_union=None)
        assert_that(condition.is_met(person), equal_to(False))

        other_student_union = StudentUnionFactory()
        person.liu_student_union = other_student_union
        assert_that(condition.is_met(person), equal_to(False))

        person.liu_student_union = student_union
        assert_that(condition.is_met(person), equal_to(True))
