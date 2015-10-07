# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Functionary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registered', models.DateTimeField(auto_now_add=True, verbose_name='registration timestamp')),
                ('ice_number', models.CharField(max_length=16, null=True, verbose_name='ICE number', blank=True)),
                ('b_driving_license', models.BooleanField(default=False, verbose_name='B driving license')),
                ('signed_contract', models.BooleanField(default=False, verbose_name='signed contract')),
                ('attended_info_meeting', models.BooleanField(default=False, verbose_name='attended info meeting')),
                ('pledge_payed', models.DateTimeField(null=True, verbose_name='pledge payed', blank=True)),
                ('pledge_returned', models.DateTimeField(null=True, verbose_name='pledge returned', blank=True)),
            ],
            options={
                'verbose_name': 'functionary',
                'verbose_name_plural': 'functionaries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('end', models.DateTimeField(verbose_name='end')),
                ('people_max', models.PositiveIntegerField(default=2, help_text="The maximum number of workers on this shift. This shift's status will be reported as overstaffed if the number of workers are over this value.", verbose_name='maximum number of workers')),
                ('people_alarming', models.PositiveIntegerField(default=1, help_text='The number of workers where the system will report the status as alarming.', verbose_name='alarming number of workers')),
                ('people_critical', models.PositiveIntegerField(default=0, help_text='The number of workers where the system will report the status as critical.', verbose_name='critical number of workers')),
                ('public', models.BooleanField(default=True, help_text="If unchecked, this shift won't be visible or available for registration by public users.", verbose_name='public')),
            ],
            options={
                'verbose_name': 'shift',
                'verbose_name_plural': 'shifts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShiftRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('checked_in', models.DateTimeField(null=True, verbose_name='checked in', blank=True)),
                ('checked_out', models.DateTimeField(null=True, verbose_name='checked out', blank=True)),
            ],
            options={
                'verbose_name': 'shift registration',
                'verbose_name_plural': 'shift registrations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShiftType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', verbose_name='parent', blank=True, to='fungus.ShiftType', null=True)),
            ],
            options={
                'verbose_name': 'shift type',
                'verbose_name_plural': 'shift types',
            },
            bases=(models.Model,),
        ),
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
    ]
