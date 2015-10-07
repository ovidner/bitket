# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conditions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoldingModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'holding modifier',
                'verbose_name_plural': 'holding modifiers',
            },
        ),
        migrations.CreateModel(
            name='ProductModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(verbose_name='order')),
                ('delta_amount', tickle.common.db.fields.MoneyField(decimal_places=2, max_digits=12, blank=True, help_text='For discount, enter a negative value.', null=True, verbose_name='delta (amount)')),
                ('delta_factor', models.DecimalField(decimal_places=2, max_digits=3, blank=True, help_text='A factor of the price (after previous modifiers). For discount, enter a negative value. E.g. -0.25 for 25% discount.', null=True, verbose_name='delta (factor)')),
                ('condition', models.ForeignKey(related_name='product_modifiers', verbose_name='condition', to='conditions.Condition')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'product modifier',
                'verbose_name_plural': 'product modifiers',
            },
        ),
    ]
