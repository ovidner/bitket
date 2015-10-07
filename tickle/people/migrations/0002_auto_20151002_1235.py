# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='stripe_customer_id',
            field=models.CharField(max_length=64, null=True, verbose_name='Stripe customer ID', blank=True),
        ),
    ]
