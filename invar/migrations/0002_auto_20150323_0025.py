# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0001_initial'),
        ('invar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicerow',
            name='holdingBackref',
            field=models.ForeignKey(to='tickle.Holding', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoicerow',
            name='invoice',
            field=models.ForeignKey(to='invar.Invoice'),
            preserve_default=True,
        ),
    ]
