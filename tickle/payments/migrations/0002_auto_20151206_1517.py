# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20151203_1439'),
        ('organizers', '0002_auto_20151201_1423'),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='cart',
            field=models.ForeignKey(verbose_name='cart', to='products.Cart', null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='organizer',
            field=models.ForeignKey(verbose_name='organizer', to='organizers.Organizer', null=True),
        ),
    ]
