# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased', models.DateTimeField(null=True, verbose_name='purchased', blank=True)),
                ('person', models.ForeignKey(related_name='carts', verbose_name='person', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(related_name='carts', verbose_name='organizer', to='organizers.Organizer')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('utilized', models.DateTimeField(null=True, verbose_name='utilized', blank=True)),
                ('purchase_price', tickle.common.db.fields.MoneyField(null=True, verbose_name='purchase price', max_digits=12, decimal_places=2, blank=True)),
                ('cart', models.ForeignKey(related_name='holdings', verbose_name='cart', to='products.Cart')),
                ('person', models.ForeignKey(related_name='holdings', verbose_name='person', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'holding',
                'verbose_name_plural': 'holdings',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', tickle.common.db.fields.NameField(max_length=64, verbose_name='name')),
                ('slug', tickle.common.db.fields.SlugField(max_length=64, verbose_name='slug')),
                ('description', tickle.common.db.fields.DescriptionField(verbose_name='description', blank=True)),
                ('base_price', tickle.common.db.fields.MoneyField(verbose_name='base price', max_digits=12, decimal_places=2)),
                ('published', models.BooleanField(default=True, verbose_name='published')),
                ('personal_limit', models.PositiveIntegerField(default=1, help_text='Blank means no limit.', null=True, verbose_name='personal limit', blank=True)),
                ('total_limit', models.PositiveIntegerField(help_text='Blank means no limit.', null=True, verbose_name='total limit', blank=True)),
                ('transferable', models.BooleanField(default=True, help_text='If people should be able to transfer this product to other people.', verbose_name='transferable')),
                ('main_event', models.ForeignKey(verbose_name='main event', to='events.MainEvent')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', tickle.common.db.fields.NameField(max_length=64, verbose_name='name')),
                ('product', models.ForeignKey(related_name='variations', verbose_name='product', to='products.Product')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'product variation',
                'verbose_name_plural': 'product variations',
            },
        ),
        migrations.CreateModel(
            name='ProductVariationChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', tickle.common.db.fields.NameField(max_length=64, verbose_name='name')),
                ('order', models.PositiveIntegerField(verbose_name='order')),
                ('product_variation', models.ForeignKey(related_name='choices', verbose_name='product variation', to='products.ProductVariation')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'product variation choice',
                'verbose_name_plural': 'product variation choices',
            },
        ),
        migrations.AddField(
            model_name='holding',
            name='product',
            field=models.ForeignKey(related_name='holdings', verbose_name='product', to='products.Product'),
        ),
        migrations.AddField(
            model_name='holding',
            name='product_variation_choices',
            field=models.ManyToManyField(related_name='holdings', verbose_name='product variation choices', to='products.ProductVariationChoice'),
        ),
        migrations.AlterUniqueTogether(
            name='productvariationchoice',
            unique_together=set([('name', 'product_variation')]),
        ),
        migrations.AlterUniqueTogether(
            name='productvariation',
            unique_together=set([('name', 'product')]),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('main_event', 'name'), ('main_event', 'slug')]),
        ),
    ]
