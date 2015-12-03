# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_cart_seller'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariationchoice',
            old_name='product_variation',
            new_name='variation',
        ),
        migrations.AlterUniqueTogether(
            name='productvariationchoice',
            unique_together=set([('name', 'variation')]),
        ),
    ]
