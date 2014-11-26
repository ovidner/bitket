# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('liu', '0002_auto_20141125_0022'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(to='tickle.Event')),
            ],
            options={
                'abstract': False,
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
                ('phone', models.CharField(max_length=32, verbose_name='phone number')),
                ('address_row_1', models.CharField(max_length=128)),
                ('liu_id', models.OneToOneField(null=True, blank=True, to='liu.LiUID', verbose_name='LiU ID')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='user account')),
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
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valid', models.BooleanField(default=True, verbose_name='valid')),
                ('holder', models.ForeignKey(verbose_name='holder', to='tickle.Person')),
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
            model_name='ticket',
            name='type',
            field=models.ForeignKey(verbose_name='type', to='tickle.TicketType'),
            preserve_default=True,
        ),
    ]
