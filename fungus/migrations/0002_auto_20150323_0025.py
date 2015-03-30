# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0001_initial'),
        ('tickle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftregistration',
            name='person',
            field=models.ForeignKey(related_name='shift_registrations', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='shift',
            field=models.ForeignKey(related_name='registrations', verbose_name='shift', to='fungus.Shift'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='location',
            field=models.ForeignKey(related_name='shifts', verbose_name='location', blank=True, to='fungus.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='responsible',
            field=models.ForeignKey(related_name='shift_responsibilities', verbose_name='responsible', blank=True, to='tickle.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='shift_type',
            field=mptt.fields.TreeForeignKey(related_name='shifts', verbose_name='shift type', to='fungus.ShiftType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', verbose_name='parent', blank=True, to='fungus.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='functionary',
            name='person',
            field=models.OneToOneField(related_name='functionary', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
            ],
            options={
                'verbose_name': 'worker',
                'proxy': True,
                'verbose_name_plural': 'workers',
            },
            bases=('tickle.person',),
        ),
    ]
