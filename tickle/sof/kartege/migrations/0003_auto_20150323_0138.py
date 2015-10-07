# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0002_create_default_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrycustommaterial',
            name='material',
            field=models.CharField(max_length=512, verbose_name='material'),
            preserve_default=True,
        ),
    ]
