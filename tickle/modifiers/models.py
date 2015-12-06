# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from tickle.common.db.fields import MoneyField, DescriptionField
from tickle.common.behaviors import NameMixin, OrderedMixin
from tickle.common.models import Model
from tickle.conditions.models import Condition


class ProductModifierQuerySet(models.QuerySet):
    def eligible(self, person, force_reevaluation=False):
        if person.is_anonymous():
            return self.none()

        return self.filter(condition__in=person.get_met_conditions(
            force_reevaluation=force_reevaluation))

    def delta(self):
        return self.aggregate(delta=models.Sum('delta_amount'))['delta'] or Decimal('0.00')


class ProductModifier(Model):
    condition = models.ForeignKey(
        'conditions.Condition',
        related_name='product_modifiers',
        verbose_name=_('condition'))
    product = models.ForeignKey(
        'products.Product',
        related_name='product_modifiers',
        verbose_name=_('product'))

    delta_amount = MoneyField(
        verbose_name=_('delta (amount)'),
        help_text=_('For discount, enter a negative value.'))

    objects = ProductModifierQuerySet.as_manager()

    class Meta:
        unique_together = [
            ['condition', 'product']
        ]

        verbose_name = _('product modifier')
        verbose_name_plural = _('product modifiers')

    def delta(self):
        return self.delta_amount

    @property
    def condition_subclass(self):
        return Condition.objects.get_subclass(id=self.condition_id)


class HoldingModifier(Model):
    product_modifier = models.ForeignKey(
        'ProductModifier',
        related_name='holding_modifiers',
        verbose_name=_('product modifier'))
    holding = models.ForeignKey(
        'products.Holding',
        related_name='holding_modifiers',
        verbose_name=_('holding'))

    class Meta:
        unique_together = [
            ['product_modifier', 'holding']
        ]

        verbose_name = _('holding modifier')
        verbose_name_plural = _('holding modifiers')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.holding.product == self.product_modifier.product:
            raise ValidationError('Impossible holding/modifier combination. '
                                  'Products not matching.')

        super(HoldingModifier, self).save(force_insert, force_update, using,
                                          update_fields)
