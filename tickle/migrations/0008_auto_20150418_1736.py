# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0007_auto_20150418_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(verbose_name='order')),
                ('discount', models.ForeignKey(related_name='product_discounts', to='tickle.Discount')),
                ('product', models.ForeignKey(related_name='discounts', verbose_name='product', to='tickle.Product')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='productdiscount',
            unique_together=set([('product', 'discount')]),
        ),
    ]
