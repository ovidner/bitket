# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modifiers', '0004_auto_20151130_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holdingmodifier',
            name='holding',
            field=models.ForeignKey(related_name='holding_modifiers', verbose_name='holding', to='products.Holding'),
        ),
    ]
