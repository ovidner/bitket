# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0004_auto_20150115_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='notes',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
