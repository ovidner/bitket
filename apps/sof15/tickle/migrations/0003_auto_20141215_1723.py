# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0002_auto_20141209_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(to='tickle.SpecialNutrition', null=True, blank=True),
            preserve_default=True,
        ),
    ]
