# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modifiers', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodifier',
            name='product',
            field=models.ForeignKey(related_name='product_modifiers', verbose_name='product', to='products.Product'),
        ),
        migrations.AddField(
            model_name='holdingmodifier',
            name='holding',
            field=models.ForeignKey(related_name='holding_modifiers', verbose_name='holding', to='products.Product'),
        ),
        migrations.AddField(
            model_name='holdingmodifier',
            name='product_modifier',
            field=models.ForeignKey(related_name='holding_modifiers', verbose_name='product modifier', to='modifiers.ProductModifier'),
        ),
        migrations.AlterUniqueTogether(
            name='productmodifier',
            unique_together=set([('condition', 'product')]),
        ),
        migrations.AlterUniqueTogether(
            name='holdingmodifier',
            unique_together=set([('product_modifier', 'holding')]),
        ),
    ]
