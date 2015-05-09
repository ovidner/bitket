# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0016_holding_transferee'),
        ('karthago', '0006_auto_20150428_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='KartegeMember',
            fields=[
            ],
            options={
                'verbose_name': 'K\xe5rtege member',
                'proxy': True,
                'verbose_name_plural': 'K\xe5rtege members',
            },
            bases=('tickle.person',),
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ('constellation',), 'verbose_name': 'entry', 'verbose_name_plural': 'entries'},
        ),
    ]
