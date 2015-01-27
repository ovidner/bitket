# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0006_auto_20150120_0023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orchestramembership',
            name='active',
        ),
    ]
