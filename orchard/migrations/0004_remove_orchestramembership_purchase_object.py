# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0003_auto_20150115_0137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orchestramembership',
            name='purchase_object',
        ),
    ]
