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
            model_name='worker',
            name='person',
            field=models.OneToOneField(related_name='worker', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shifttype',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='fungus.ShiftType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='shift',
            field=models.ForeignKey(to='fungus.Shift'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='worker',
            field=models.ForeignKey(to='fungus.Worker'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='responsible',
            field=models.ForeignKey(related_name='shift_responsibilities', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shift',
            name='shift_type',
            field=mptt.fields.TreeForeignKey(related_name='shifts', to='fungus.ShiftType'),
            preserve_default=True,
        ),
    ]
