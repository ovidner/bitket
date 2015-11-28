# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from tickle.common.db.fields import MoneyField, DescriptionField
from tickle.common.behaviors import NameMixin, OrderedMixin


class ProductModifierQuerySet(models.QuerySet):
    def met(self, person):
        met_pks = []
        for condition in person.met_conditions():
            for product_modifier in condition.product_modifiers:
                met_pks.append(product_modifier.pk)

        return self.filter(pk__in=met_pks)

    def total_delta(self):
        total_delta = Decimal(0)
        for i in self:
            total_delta += i.delta()
        return total_delta



class ProductModifier(OrderedMixin, models.Model):
    condition = models.ForeignKey(
        'conditions.Condition',
        related_name='product_modifiers',
        verbose_name=_('condition'))
    product = models.ForeignKey(
        'products.Product',
        related_name='product_modifiers',
        verbose_name=_('product'))

    delta_amount = MoneyField(
        null=True,
        blank=True,
        verbose_name=_('delta (amount)'),
        help_text=_('For discount, enter a negative value.'))

    objects = ProductModifierQuerySet.as_manager()

    class Meta:
        ordering = ['order']
        unique_together = [
            ['condition', 'product']
        ]

        verbose_name = _('product modifier')
        verbose_name_plural = _('product modifiers')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if ((self.delta_amount and self.delta_factor) or
                (not self.delta_amount and not self.delta_factor)):
            raise ValidationError(_("Please specify amount or percent."))

        super(ProductModifier, self).save(force_insert, force_update, using,
                                          update_fields)

    def delta(self):
        return self.delta_amount


class HoldingModifier(models.Model):
    product_modifier = models.ForeignKey(
        'ProductModifier',
        related_name='holding_modifiers',
        verbose_name=_('product modifier'))
    holding = models.ForeignKey(
        'products.Product',
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
        if not self.holding.product != self.product_modifier.product:
            raise ValidationError('Impossible holding/modifier combination. '
                                  'Products not matching.')

        super(HoldingModifier, self).save(force_insert, force_update, using,
                                          update_fields)


class ProductDiscountQuerySet(models.QuerySet):
    def copy_to_holding_discounts(self, holding):
        for i in self:
            HoldingDiscount.objects.create(holding=holding, discount=i.discount, order=i.order)
