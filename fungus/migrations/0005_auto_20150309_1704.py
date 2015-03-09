# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0004_shifttype_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='people_alarming',
            field=models.PositiveIntegerField(default=1, help_text='The number of workers where the system will report the status as alarming.', verbose_name='alarming number of workers'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shift',
            name='people_critical',
            field=models.PositiveIntegerField(default=0, help_text='The number of workers where the system will report the status as critical.', verbose_name='critical number of workers'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shift',
            name='people_max',
            field=models.PositiveIntegerField(default=2, help_text="The maximum number of workers on this shift. This shift's status will be reported as overstaffed if the number of workers are over this value.", verbose_name='maximum number of workers'),
            preserve_default=True,
        ),
    ]
