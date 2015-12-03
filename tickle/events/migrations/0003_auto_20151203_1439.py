# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151201_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainevent',
            name='organizer',
            field=models.ForeignKey(related_name='events', verbose_name='organizer', to='organizers.Organizer'),
        ),
    ]
