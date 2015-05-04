# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0004_auto_20150420_0243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shift',
            options={'ordering': ('shift_type', 'start', 'end'), 'verbose_name': 'shift', 'verbose_name_plural': 'shifts'},
        ),
        migrations.AlterModelOptions(
            name='shifttype',
            options={'ordering': ('name',), 'verbose_name': 'shift type', 'verbose_name_plural': 'shift types'},
        ),
    ]
