# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0011_auto_20150428_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quota',
            field=models.PositiveIntegerField(default=0, verbose_name='quota'),
        ),
    ]
