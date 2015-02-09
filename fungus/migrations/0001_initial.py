# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0008_auto_20150202_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='fungus.Location', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('people_max', models.PositiveIntegerField(null=True, verbose_name='maximum number of workers', blank=True)),
                ('people_warning', models.PositiveIntegerField(null=True, verbose_name='warning number of workers', blank=True)),
                ('people_critical', models.PositiveIntegerField(help_text='The number of workers needed on this shift for critical operation.', null=True, verbose_name='critical number of workers', blank=True)),
                ('public', models.BooleanField(default=True, help_text="If unchecked, this shift won't be visible or available for registration by public users.", verbose_name='public')),
                ('location', models.ForeignKey(related_name='shifts', blank=True, to='fungus.Location', null=True)),
                ('responsible', models.ForeignKey(related_name='shift_responsibilities', blank=True, to='tickle.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShiftRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.ForeignKey(related_name='shift_registrations', to='tickle.Person')),
                ('shift', models.ForeignKey(related_name='registrations', to='fungus.Shift')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShiftType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='fungus.ShiftType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ice_number', models.CharField(max_length=16, null=True, verbose_name='ICE number', blank=True)),
                ('person', models.OneToOneField(related_name='worker', to='tickle.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shift',
            name='shift_type',
            field=mptt.fields.TreeForeignKey(related_name='shifts', to='fungus.ShiftType'),
            preserve_default=True,
        ),
    ]
