# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0004_auto_20150119_1506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='type',
            new_name='entry_type',
        ),
    ]
