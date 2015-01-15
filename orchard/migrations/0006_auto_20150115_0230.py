# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0005_auto_20150115_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orchestramembership',
            name='active',
            field=models.BooleanField(default=False, verbose_name='active member'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramembership',
            name='primary',
            field=models.BooleanField(default=False, verbose_name='primary orchestra'),
            preserve_default=True,
        ),
    ]
