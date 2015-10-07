from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy

from tickle.people.factories import StudentUnionFactory
from .models import Condition, StudentUnionMemberCondition


class ConditionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Condition


class StudentUnionMemberConditionFactory(ConditionFactory):
    student_union = factory.SubFactory(StudentUnionFactory)

    class Meta:
        model = StudentUnionMemberCondition
