# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0009_auto_20150420_0243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('name',), 'verbose_name': 'event', 'verbose_name_plural': 'events'},
        ),
        migrations.RemoveField(
            model_name='event',
            name='level',
        ),
        migrations.RemoveField(
            model_name='event',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='event',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='event',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='events',
            field=models.ManyToManyField(related_name='ticket_types', verbose_name='events', to='tickle.Event', blank=True),
        ),
    ]
