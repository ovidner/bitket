# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0002_auto_20150323_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='functionary',
            name='b_driving_license',
            field=models.BooleanField(default=False, help_text='Mandatory for driving missions.', verbose_name='B driving license'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='functionary',
            name='registered',
            field=models.DateTimeField(verbose_name='registration timestamp', blank=True),
            preserve_default=True,
        ),
    ]
