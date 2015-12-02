from __future__ import absolute_import, unicode_literals

from django.db import models

from model_utils.managers import InheritanceQuerySetMixin


class ConditionQuerySet(InheritanceQuerySetMixin, models.QuerySet):
    def met(self, person):
        met_pks = []

        for condition in self.select_subclasses():
            if condition.is_met(person):
                met_pks.append(condition.pk)

        return self.filter(pk__in=met_pks)
