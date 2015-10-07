# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0004_auto_20150407_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='approved'),
        ),
    ]
