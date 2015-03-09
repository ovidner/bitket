# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0003_auto_20150302_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifttype',
            name='description',
            field=models.TextField(null=True, verbose_name='shift description', blank=True),
            preserve_default=True,
        ),
    ]
