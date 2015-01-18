# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0002_auto_20150118_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orchestra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
                'permissions': (('approve_members', 'Approve members'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrchestraMemberRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchase', models.ForeignKey(related_name='orchestra_member_registrations', to='tickle.Purchase')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrchestraMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False, verbose_name='active member')),
                ('primary', models.BooleanField(default=False, verbose_name='primary orchestra')),
                ('approved', models.NullBooleanField()),
                ('orchestra', models.ForeignKey(related_name='memberships', to='orchard.Orchestra')),
                ('person', models.ForeignKey(related_name='memberships', to='tickle.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrchestraTicketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accommodation_ticket_type', models.ForeignKey(related_name='+', blank=True, to='tickle.TicketType', null=True)),
                ('dinner_ticket_type', models.ForeignKey(related_name='+', blank=True, to='tickle.TicketType', null=True)),
                ('food_ticket_type', models.ForeignKey(related_name='+', blank=True, to='tickle.TicketType', null=True)),
                ('ticket_type', models.OneToOneField(related_name='orchestra_ticket_type', to='tickle.TicketType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='orchestramembership',
            unique_together=set([('orchestra', 'person')]),
        ),
        migrations.AddField(
            model_name='orchestra',
            name='members',
            field=models.ManyToManyField(related_name='orchestras', through='orchard.OrchestraMembership', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='OrchestraProduct',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('tickle.product',),
        ),
    ]
