# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0010_auto_20150223_0056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AddField(
            model_name='product',
            name='published',
            field=models.BooleanField(default=True, verbose_name='published'),
            preserve_default=True,
        ),
    ]
