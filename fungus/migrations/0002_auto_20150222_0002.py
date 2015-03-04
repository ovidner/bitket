# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('discount_amount', models.DecimalField(null=True, verbose_name='amount', max_digits=9, decimal_places=2, blank=True)),
                ('discount_percent', models.DecimalField(null=True, verbose_name='percent', max_digits=3, decimal_places=2, blank=True)),
                ('shifts', models.PositiveIntegerField(help_text='Number of shifts to work to be eligible for this discount.', verbose_name='shifts')),
            ],
            options={
                'verbose_name': 'worker discount',
                'verbose_name_plural': 'worker discounts',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'location', 'verbose_name_plural': 'locations'},
        ),
        migrations.AlterModelOptions(
            name='shift',
            options={'verbose_name': 'shift', 'verbose_name_plural': 'shifts'},
        ),
        migrations.AlterModelOptions(
            name='shiftregistration',
            options={'verbose_name': 'shift registration', 'verbose_name_plural': 'shift registrations'},
        ),
        migrations.AlterModelOptions(
            name='shifttype',
            options={'verbose_name': 'shift type', 'verbose_name_plural': 'shift types'},
        ),
        migrations.AlterModelOptions(
            name='worker',
            options={'verbose_name': 'worker', 'verbose_name_plural': 'workers'},
        ),
    ]
