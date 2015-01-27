# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orchestratickettype',
            name='accommodation_ticket_type',
            field=models.ForeignKey(related_name='+', default=1, to='tickle.TicketType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='dinner_ticket_type',
            field=models.ForeignKey(related_name='+', default=1, to='tickle.TicketType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='food_ticket_type',
            field=models.ForeignKey(related_name='+', default=1, to='tickle.TicketType'),
            preserve_default=False,
        ),
    ]
