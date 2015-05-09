# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0014_convert_liu_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='invalidated',
            field=models.BooleanField(default=False, verbose_name='invalidated'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='last name', blank=True),
        ),
    ]
