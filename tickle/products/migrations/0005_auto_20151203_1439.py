# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productvariationchoice_delta_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_event',
            field=models.ForeignKey(related_name='products', verbose_name='main event', to='events.MainEvent'),
        ),
    ]
