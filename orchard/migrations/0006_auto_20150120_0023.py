# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0005_auto_20150120_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orchestratickettype',
            name='accommodation_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='accommodation ticket type', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='dinner_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='dinner ticket type', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestratickettype',
            name='food_ticket_type',
            field=models.ForeignKey(related_name='+', verbose_name='food ticket type', blank=True, to='tickle.TicketType', null=True),
            preserve_default=True,
        ),
    ]
