# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='limit',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantitative',
        ),
        migrations.AddField(
            model_name='product',
            name='personal_limit',
            field=models.PositiveIntegerField(help_text='Blank means no limit.', null=True, verbose_name='personal limit', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='total_limit',
            field=models.PositiveIntegerField(help_text='Blank means no limit.', null=True, verbose_name='total limit', blank=True),
        ),
    ]
