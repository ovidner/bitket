# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20151001_1305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='organizer',
            new_name='seller',
        ),
    ]
