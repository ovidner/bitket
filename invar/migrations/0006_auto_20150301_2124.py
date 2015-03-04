# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0010_auto_20150223_0056'),
        ('invar', '0005_auto_20150224_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicerow',
            name='holdingBackref',
            field=models.ForeignKey(to='tickle.Holding', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='create_date',
            field=models.DateField(default=datetime.date(2015, 3, 1), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.date(2015, 3, 15)),
            preserve_default=True,
        ),
    ]
