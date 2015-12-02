# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('modifiers', '0003_remove_productmodifier_delta_factor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productmodifier',
            options={'verbose_name': 'product modifier', 'verbose_name_plural': 'product modifiers'},
        ),
        migrations.RemoveField(
            model_name='productmodifier',
            name='order',
        ),
        migrations.AlterField(
            model_name='productmodifier',
            name='delta_amount',
            field=tickle.common.db.fields.MoneyField(default='0.00', help_text='For discount, enter a negative value.', verbose_name='delta (amount)', max_digits=12, decimal_places=2),
            preserve_default=False,
        ),
    ]
