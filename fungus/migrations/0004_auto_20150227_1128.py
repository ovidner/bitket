# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0003_auto_20150227_0943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worker',
            options={'verbose_name': 'worker', 'verbose_name_plural': 'workers'},
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='checked_in',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='checked_out',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
