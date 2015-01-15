# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0005_auto_20150115_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='special_nutrition_notes',
            field=models.CharField(max_length=256, blank=True),
            preserve_default=True,
        ),
    ]
