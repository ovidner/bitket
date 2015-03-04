# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0014_auto_20150224_0038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orchestraproduct',
            options={'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]
