# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0002_auto_20150407_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickleuser',
            name='username',
        ),
        migrations.RenameField(
            model_name='tickleuser',
            old_name='is_admin',
            new_name='is_staff',
        ),
    ]
