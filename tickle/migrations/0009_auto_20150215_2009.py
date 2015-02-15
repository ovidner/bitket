# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0008_auto_20150202_0003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='delivery',
            options={'verbose_name': 'delivery', 'verbose_name_plural': 'deliveries'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'event', 'verbose_name_plural': 'events'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'verbose_name': 'purchase', 'verbose_name_plural': 'purchases'},
        ),
        migrations.AlterModelOptions(
            name='tickettype',
            options={'verbose_name': 'ticket type', 'verbose_name_plural': 'ticket types'},
        ),
    ]
