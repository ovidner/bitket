# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0007_auto_20150126_1652'),
        ('orchard', '0007_remove_orchestramembership_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orchestramemberregistration',
            options={'verbose_name': 'orchestra member registration', 'verbose_name_plural': 'orchestra member registrations'},
        ),
        migrations.AlterModelOptions(
            name='orchestratickettype',
            options={'verbose_name': 'orchestra ticket type', 'verbose_name_plural': 'orchestra ticket types'},
        ),
        migrations.RemoveField(
            model_name='orchestratickettype',
            name='dinner_ticket_type',
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
    ]
