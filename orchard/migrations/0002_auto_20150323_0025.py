# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0001_initial'),
        ('tickle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orchestratickettype',
            name='accommodation_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='accommodation ticket type', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestratickettype',
            name='food_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='food ticket type', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestratickettype',
            name='jubilarian_10_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='10th festival ticket type', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestratickettype',
            name='jubilarian_25_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='25th festival ticket type', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestratickettype',
            name='ticket_type',
            field=models.OneToOneField(related_name='orchestra_ticket_type', verbose_name='ticket type', to='tickle.TicketType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='orchestra',
            field=models.ForeignKey(related_name='memberships', verbose_name='orchestra', to='orchard.Orchestra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='person',
            field=models.ForeignKey(related_name='orchestra_memberships', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orchestramembership',
            unique_together=set([('orchestra', 'person')]),
        ),
        migrations.AddField(
            model_name='orchestramemberregistration',
            name='purchase',
            field=models.OneToOneField(related_name='orchestra_member_registration', verbose_name='purchase', to='tickle.Purchase'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestra',
            name='contact',
            field=models.ForeignKey(related_name='orchestra_contacts', verbose_name='contact', blank=True, to='tickle.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestra',
            name='members',
            field=models.ManyToManyField(related_name='orchestras', verbose_name='members', through='orchard.OrchestraMembership', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='OrchardPerson',
            fields=[
            ],
            options={
                'verbose_name': 'orchestra member',
                'proxy': True,
                'verbose_name_plural': 'orchestra members',
            },
            bases=('tickle.person',),
        ),
        migrations.CreateModel(
            name='OrchestraProduct',
            fields=[
            ],
            options={
                'verbose_name': 'product',
                'proxy': True,
                'verbose_name_plural': 'products',
            },
            bases=('tickle.product',),
        ),
    ]
