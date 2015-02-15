# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0002_auto_20150118_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orchestra',
            options={'ordering': ['name'], 'verbose_name': 'orchestra', 'verbose_name_plural': 'orchestras', 'permissions': (('approve_orchestra_members', 'Approve orchestra members'),)},
        ),
        migrations.AlterModelOptions(
            name='orchestramembership',
            options={'verbose_name': 'orchestra membership', 'verbose_name_plural': 'orchestra memberships'},
        ),
        migrations.AlterField(
            model_name='orchestra',
            name='members',
            field=models.ManyToManyField(related_name='orchestras', verbose_name='members', through='orchard.OrchestraMembership', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestra',
            name='name',
            field=models.CharField(max_length=256, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramemberregistration',
            name='purchase',
            field=models.ForeignKey(related_name='orchestra_member_registrations', verbose_name='purchase', to='tickle.Purchase'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramembership',
            name='orchestra',
            field=models.ForeignKey(related_name='memberships', verbose_name='orchestra', to='orchard.Orchestra'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramembership',
            name='person',
            field=models.ForeignKey(related_name='memberships', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='accommodation_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='accommodation ticket type', to='tickle.TicketType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='dinner_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='dinner ticket type', to='tickle.TicketType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='food_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='food ticket type', to='tickle.TicketType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='ticket_type',
            field=models.OneToOneField(related_name='orchestra_ticket_type', verbose_name='ticket type', to='tickle.TicketType'),
            preserve_default=True,
        ),
    ]
