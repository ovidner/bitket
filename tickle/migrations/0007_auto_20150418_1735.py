# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tickle', '0006_auto_20150414_0925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='object id')),
                ('content_type', models.ForeignKey(verbose_name='content type', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'discount',
                'verbose_name_plural': 'discounts',
            },
        ),
        migrations.CreateModel(
            name='DiscountEligibility',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discount', models.ForeignKey(related_name='eligibilities', to='tickle.Discount')),
                ('person', models.ForeignKey(related_name='discount_eligibilities', to='tickle.Person')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.OneToOneField(related_name='shopping_cart', verbose_name='person', to='tickle.Person')),
            ],
            options={
                'verbose_name': 'shopping cart',
                'verbose_name_plural': 'shopping carts',
            },
        ),
        migrations.RemoveField(
            model_name='productdiscount',
            name='discount_content_type',
        ),
        migrations.RemoveField(
            model_name='productdiscount',
            name='product',
        ),
        migrations.RemoveField(
            model_name='studentuniondiscount',
            name='name',
        ),
        migrations.AddField(
            model_name='holding',
            name='transferable',
            field=models.BooleanField(default=True, help_text='If people should be able to transfer this product to other people. Note: setting this to false overrides the product setting. Setting this to true will not override product setting.', verbose_name='transferable'),
        ),
        migrations.AddField(
            model_name='product',
            name='transferable',
            field=models.BooleanField(default=True, help_text='If people should be able to transfer this product to other people.', verbose_name='transferable'),
        ),
        migrations.AlterField(
            model_name='studentuniondiscount',
            name='discount_percent',
            field=models.DecimalField(decimal_places=2, max_digits=3, blank=True, help_text='Use decimal form, e.g. 0,25.', null=True, verbose_name='percent'),
        ),
        migrations.DeleteModel(
            name='ProductDiscount',
        ),
        migrations.AddField(
            model_name='holding',
            name='shopping_cart',
            field=models.ForeignKey(related_name='holdings', verbose_name='shopping cart', blank=True, to='tickle.ShoppingCart', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='discounteligibility',
            unique_together=set([('discount', 'person')]),
        ),
        migrations.AlterUniqueTogether(
            name='discount',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
