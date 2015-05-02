# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0012_product_quota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='liu_id',
            field=models.CharField(default=None, max_length=10, null=True, verbose_name='LiU ID', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quota',
            field=models.PositiveIntegerField(default=0, help_text='0 means there is no quota limit.', verbose_name='quota', blank=True),
        ),
    ]
