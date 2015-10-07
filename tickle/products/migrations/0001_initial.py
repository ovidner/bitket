# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased', models.DateTimeField(null=True, verbose_name='purchased', blank=True)),
                ('organizer', models.ForeignKey(related_name='carts', verbose_name='organizer', to='events.Organizer')),
                ('person', models.ForeignKey(related_name='carts', verbose_name='person', to=settings.AUTH_USER_MODEL)),
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
                ('utilized', models.DateTimeField(default=django.utils.timezone.now, verbose_name='utilized')),
                ('purchase_price', tickle.common.db.fields.MoneyField(max_digits=12, decimal_places=2)),
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
                ('quantitative', models.BooleanField(default=False, help_text='Can you purchase more than one (1) of this product?', verbose_name='quantitative')),
                ('published', models.BooleanField(default=True, verbose_name='published')),
                ('limit', models.PositiveIntegerField(help_text='Blank means no limit.', null=True, verbose_name='quantity limit', blank=True)),
                ('transferable', models.BooleanField(default=True, help_text='If people should be able to transfer this product to other people.', verbose_name='transferable')),
                ('main_event', models.ForeignKey(verbose_name='main event', to='events.MainEvent')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.AddField(
            model_name='holding',
            name='product',
            field=models.ForeignKey(related_name='holdings', verbose_name='product', to='products.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('main_event', 'name'), ('main_event', 'slug')]),
        ),
    ]
