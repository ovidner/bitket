# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0009_auto_20150129_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='orchestra',
            name='orgNr',
            field=models.CharField(max_length=256, null=True, verbose_name='org_nr'),
            preserve_default=True,
        ),
    ]
