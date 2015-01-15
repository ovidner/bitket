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
            field=models.ForeignKey(related_name='orchestra_ticket_type_accommodation', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestratickettype',
            name='food_ticket_type',
            field=models.ForeignKey(related_name='orchestra_ticket_type_food', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestratickettype',
            name='ticket_type',
            field=models.OneToOneField(related_name='orchestra_ticket_type', to='tickle.TicketType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='member',
            field=models.ForeignKey(related_name='memberships', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='orchestra',
            field=models.ForeignKey(related_name='memberships', to='orchard.Orchestra'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='orchestramembership',
            unique_together=set([('orchestra', 'member')]),
        ),
        migrations.AddField(
            model_name='orchestramember',
            name='person',
            field=models.OneToOneField(related_name='orchestra_member', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestra',
            name='members',
            field=models.ManyToManyField(related_name='orchestras', through='orchard.OrchestraMembership', to='tickle.Person'),
            preserve_default=True,
        ),
    ]
