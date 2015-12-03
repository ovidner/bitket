# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20151126_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariationchoice',
            name='delta_amount',
            field=tickle.common.db.fields.MoneyField(default=Decimal('0'), help_text='For discount, enter a negative value.', verbose_name='delta (amount)', max_digits=12, decimal_places=2),
        ),
    ]
