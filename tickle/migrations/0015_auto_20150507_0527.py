# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0014_convert_liu_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='delivered',
        ),
        migrations.AddField(
            model_name='delivery',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='holdings',
            field=models.ManyToManyField(related_name='deliveries', verbose_name='holdings', to='tickle.Holding'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='first name', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='last name', blank=True),
        ),
    ]
