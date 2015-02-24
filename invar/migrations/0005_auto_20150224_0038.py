# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0004_auto_20150215_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='create_date',
            field=models.DateField(default=datetime.date(2015, 2, 24), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.date(2015, 3, 10)),
            preserve_default=True,
        ),
    ]
