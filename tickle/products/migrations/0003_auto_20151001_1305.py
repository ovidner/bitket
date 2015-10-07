# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20151001_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holding',
            name='purchase_price',
            field=tickle.common.db.fields.MoneyField(null=True, verbose_name='purchase price', max_digits=12, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='personal_limit',
            field=models.PositiveIntegerField(default=1, help_text='Blank means no limit.', null=True, verbose_name='personal limit', blank=True),
        ),
    ]
