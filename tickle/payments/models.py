# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ungettext_lazy, ugettext_lazy as _
from django.db import models
from django.utils.timezone import now


class Transaction(models.Model):
    timestamp = models.DateTimeField(
        default=now,
        verbose_name=_('timestamp'))
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_('amount'))
    stripe_charge = models.CharField(
        max_length=64,
        verbose_name=_('Stripe charge'))

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

