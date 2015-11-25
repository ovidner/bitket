# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='liu_card_magnet',
        ),
        migrations.RemoveField(
            model_name='person',
            name='liu_id_blocked',
        ),
        migrations.AlterField(
            model_name='person',
            name='liu_card_rfid',
            field=models.CharField(max_length=32, verbose_name='LiU card number', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='liu_id',
            field=tickle.common.db.fields.NullCharField(null=True, default=None, max_length=8, blank=True, unique=True, verbose_name='LiU ID'),
        ),
        migrations.AlterField(
            model_name='person',
            name='pid_code',
            field=tickle.common.db.fields.NullCharField(default=None, max_length=4, blank=True, help_text='Last 4 digits in Swedish national identity number.', null=True, verbose_name='national identity code'),
        ),
    ]
