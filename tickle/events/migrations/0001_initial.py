# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', tickle.common.db.fields.NameField(max_length=64, verbose_name='name')),
                ('slug', tickle.common.db.fields.SlugField(max_length=64, verbose_name='slug')),
                ('description', tickle.common.db.fields.DescriptionField(verbose_name='description', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', tickle.common.db.fields.NameField(unique=True, max_length=64, verbose_name='name')),
                ('slug', tickle.common.db.fields.SlugField(unique=True, max_length=64, verbose_name='slug')),
                ('stripe_account_id', models.CharField(max_length=32, verbose_name='Stripe account ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='mainevent',
            name='organizer',
            field=models.ForeignKey(verbose_name='organizer', to='events.Organizer'),
        ),
        migrations.AlterUniqueTogether(
            name='mainevent',
            unique_together=set([('organizer', 'name'), ('organizer', 'slug')]),
        ),
    ]
