from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .querysets import ConditionQuerySet


@python_2_unicode_compatible
class Condition(models.Model):
    active = models.BooleanField(
        default=True,
        verbose_name=_('active'),
        help_text=_('Determines whether the condition should be displayed and '
                    'included in queries.'))

    objects = ConditionQuerySet.as_manager()

    type_str = _('condition')

    class Meta:
        verbose_name = _('condition')
        verbose_name_plural = _('conditions')

    def __str__(self):
        return '{0}: {1}'.format(self.type_str, self.condition_str)

    @property
    def condition_str(self):
        return ''

    def is_met(self, person):
        raise Exception('is_met method not overridden or incorrectly called.')


class StudentUnionMemberCondition(Condition):
    student_union = models.ForeignKey(
        'people.StudentUnion',
        related_name='+',
        verbose_name=_('student union'))

    type_str = _('student union member')

    class Meta:
        verbose_name = _('student union member condition')
        verbose_name_plural = _('student union member conditions')

    def condition_str(self):
        return '{}'.format(self.student_union)

    def is_met(self, person):
        return person.liu_student_union_id == self.student_union_id
