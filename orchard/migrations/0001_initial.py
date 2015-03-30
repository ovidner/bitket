# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orchestra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('organisation_number', models.CharField(default='', max_length=11, verbose_name='organisation number', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'orchestra',
                'verbose_name_plural': 'orchestras',
                'permissions': (('approve_orchestra_members', 'Approve orchestra members'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrchestraMemberRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'orchestra member registration',
                'verbose_name_plural': 'orchestra member registrations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrchestraMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primary', models.BooleanField(default=False, verbose_name='primary orchestra')),
                ('approved', models.NullBooleanField()),
            ],
            options={
                'verbose_name': 'orchestra membership',
                'verbose_name_plural': 'orchestra memberships',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrchestraTicketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'orchestra ticket type',
                'verbose_name_plural': 'orchestra ticket types',
            },
            bases=(models.Model,),
        ),
    ]
