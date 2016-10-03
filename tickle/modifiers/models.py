# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from tickle.common.db.fields import MoneyField
from tickle.common.behaviors import NameMixin, OrderedMixin
from tickle.common.models import Model
from tickle.conditions.models import Condition


class ModifierQuerySet(models.QuerySet):
    def eligible(self, person, force_reevaluation=False):
        if person.is_anonymous():
            return self.none()

        return self.filter(condition__in=person.get_met_conditions(
            force_reevaluation=force_reevaluation))

    def delta(self):
        return self.aggregate(delta=models.Sum('delta_amount'))['delta'] or Decimal('0.00')


@python_2_unicode_compatible
class Modifier(Model):
    condition = models.ForeignKey(
        'conditions.Condition',
        related_name='product_modifiers',
        verbose_name=_('condition'))

    delta_amount = MoneyField(
        verbose_name=_('delta (amount)'),
        help_text=_('For discount, enter a negative value.'))

    objects = ModifierQuerySet.as_manager()

    class Meta:
        verbose_name = _('modifier')
        verbose_name_plural = _('modifiers')

    def __str__(self):
        return self.condition

    def delta(self):
        return self.delta_amount

    @property
    def condition_subclass(self):
        return Condition.objects.get_subclass(id=self.condition_id)
