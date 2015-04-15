# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0005_auto_20150413_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='pid_coordination',
            field=models.BooleanField(default=False, help_text='Designates if national identity number is a <em>samordningsnummer</em>.', verbose_name='coordination number'),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('birth_date', 'pid_code', 'pid_coordination')]),
        ),
    ]
