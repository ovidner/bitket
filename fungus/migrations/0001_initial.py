# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0007_auto_20150126_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('min_workers', models.PositiveIntegerField(default=1, help_text='The number of workers needed on this shift for critical operation.', verbose_name='minimum number of workers')),
                ('max_workers', models.PositiveIntegerField(verbose_name='maximum number of workers')),
                ('public', models.BooleanField(default=True, help_text="If unchecked, this shift won't be visible or available for registration by public users.", verbose_name='public')),
                ('responsible', models.ForeignKey(related_name='shift_responsibilities', to='tickle.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShiftRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shift', models.ForeignKey(to='fungus.Shift')),
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
                ('ice_number', models.CharField(max_length=16, verbose_name='ICE number')),
                ('person', models.OneToOneField(related_name='worker', to='tickle.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='worker',
            field=models.ForeignKey(to='fungus.Worker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='shift_type',
            field=mptt.fields.TreeForeignKey(related_name='shifts', to='fungus.ShiftType'),
            preserve_default=True,
        ),
    ]
