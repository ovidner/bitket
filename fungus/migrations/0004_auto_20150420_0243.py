# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0003_auto_20150330_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionaryDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discount_amount', models.DecimalField(null=True, verbose_name='amount', max_digits=9, decimal_places=2, blank=True)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=3, blank=True, help_text='Use decimal form, e.g. 0,25.', null=True, verbose_name='percent')),
                ('shifts', models.PositiveIntegerField(help_text='Number of shifts to work to be eligible for this discount.', verbose_name='shifts')),
            ],
            options={
                'ordering': ('shifts',),
                'verbose_name': 'functionary discount',
                'verbose_name_plural': 'functionary discounts',
            },
        ),
        migrations.DeleteModel(
            name='WorkerDiscount',
        ),
    ]
