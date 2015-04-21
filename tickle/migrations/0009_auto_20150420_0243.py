# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0008_auto_20150418_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountTeaser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='text')),
            ],
        ),
        migrations.CreateModel(
            name='HoldingDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(verbose_name='order')),
                ('discount', models.ForeignKey(related_name='holding_discounts', verbose_name='discount', to='tickle.Discount')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'holding discount',
                'verbose_name_plural': 'holding discounts',
            },
        ),
        migrations.AlterModelOptions(
            name='discounteligibility',
            options={'verbose_name': 'discount eligibility', 'verbose_name_plural': 'discount eligibilities'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('order',), 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterModelOptions(
            name='productdiscount',
            options={'ordering': ('order',), 'verbose_name': 'product discount', 'verbose_name_plural': 'product discounts'},
        ),
        migrations.RemoveField(
            model_name='holding',
            name='transferable',
        ),
        migrations.AddField(
            model_name='holding',
            name='_transferable',
            field=models.NullBooleanField(default=None, help_text='If people should be able to transfer this product to other people. Note: this will override the product setting.', verbose_name='transferable'),
        ),
        migrations.AddField(
            model_name='product',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productdiscount',
            name='discount',
            field=models.ForeignKey(related_name='product_discounts', verbose_name='discount', to='tickle.Discount'),
        ),
        migrations.AlterField(
            model_name='productdiscount',
            name='product',
            field=models.ForeignKey(related_name='product_discounts', verbose_name='product', to='tickle.Product'),
        ),
        migrations.AddField(
            model_name='holdingdiscount',
            name='holding',
            field=models.ForeignKey(related_name='holding_discounts', verbose_name='holding', to='tickle.Holding'),
        ),
        migrations.AddField(
            model_name='discountteaser',
            name='product',
            field=models.ForeignKey(related_name='discount_teasers', verbose_name='product', to='tickle.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='holdingdiscount',
            unique_together=set([('holding', 'discount')]),
        ),
    ]
