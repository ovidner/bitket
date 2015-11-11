# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', tickle.common.db.fields.NameField(max_length=64, verbose_name='name')),
                ('slug', tickle.common.db.fields.SlugField(max_length=64, verbose_name='slug')),
                ('description', tickle.common.db.fields.DescriptionField(verbose_name='description', blank=True)),
                ('organizer', models.ForeignKey(verbose_name='organizer', to='organizers.Organizer')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.AlterUniqueTogether(
            name='mainevent',
            unique_together=set([('organizer', 'name'), ('organizer', 'slug')]),
        ),
    ]
