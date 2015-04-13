# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0004_auto_20150413_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(help_text='Specify any special nutritional needs or habits.', to='tickle.SpecialNutrition', verbose_name='special nutrition', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='tickle.Category', verbose_name='categories', blank=True),
        ),
    ]
