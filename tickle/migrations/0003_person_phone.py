# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0002_purchase_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone',
            field=models.CharField(max_length=24, null=True, verbose_name=b'phone number', blank=True),
            preserve_default=True,
        ),
    ]
