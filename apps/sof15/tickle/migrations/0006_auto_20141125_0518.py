# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0005_auto_20141125_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='address_row_2',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
