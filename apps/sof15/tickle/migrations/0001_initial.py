# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('liu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivered', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='tickle.Event', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=256, verbose_name='first name')),
                ('last_name', models.CharField(max_length=256, verbose_name='last name')),
                ('id_number', models.CharField(unique=True, max_length=11, verbose_name='national identification number')),
                ('phone', models.CharField(max_length=32, verbose_name='mobile number')),
                ('address_row_1', models.CharField(max_length=128)),
                ('address_row_2', models.CharField(max_length=128, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=8)),
                ('city', models.CharField(max_length=64)),
                ('liu_id', models.OneToOneField(null=True, blank=True, to='liu.LiUID', verbose_name='LiU ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('price', models.PositiveIntegerField(verbose_name='price')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased', models.DateTimeField()),
                ('holdings', models.ManyToManyField(to='tickle.Holding')),
                ('person', models.ForeignKey(to='tickle.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialNutrition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('product_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tickle.Product')),
                ('event', models.ForeignKey(verbose_name='event', to='tickle.Event')),
            ],
            options={
            },
            bases=('tickle.product',),
        ),
        migrations.AddField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(to='tickle.SpecialNutrition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='user account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='holding',
            name='person',
            field=models.ForeignKey(to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='holding',
            name='product',
            field=models.ForeignKey(to='tickle.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='delivery',
            name='holdings',
            field=models.ManyToManyField(to='tickle.Holding'),
            preserve_default=True,
        ),
    ]
