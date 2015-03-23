# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0011_auto_20150303_0125'),
        ('orchard', '0015_auto_20150303_0125'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrchardPerson',
            fields=[
            ],
            options={
                'verbose_name': 'orchestra member',
                'proxy': True,
                'verbose_name_plural': 'orchestra members',
            },
            bases=('tickle.person',),
        ),
    ]
