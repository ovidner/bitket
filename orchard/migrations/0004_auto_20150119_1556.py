# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0003_auto_20150119_1506'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orchestra',
            options={'ordering': ['name'], 'verbose_name': 'orchestra', 'verbose_name_plural': 'orchestras', 'permissions': (('approve_orchestra_members', 'Approve orchestra members'),)},
        ),
    ]
