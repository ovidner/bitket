# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0005_auto_20150423_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionaryShiftTypeDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discount_amount', models.DecimalField(null=True, verbose_name='amount', max_digits=9, decimal_places=2, blank=True)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=3, blank=True, help_text='Use decimal form, e.g. 0,25.', null=True, verbose_name='percent')),
                ('text', models.CharField(max_length=256, verbose_name='text')),
                ('shift_types', models.ManyToManyField(related_name='shift_type_discounts', verbose_name='shift types', to='fungus.ShiftType')),
            ],
            options={
                'ordering': ('text',),
                'verbose_name': 'shift type discount',
                'verbose_name_plural': 'shift type discounts',
            },
        ),
    ]
