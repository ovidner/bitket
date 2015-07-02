# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0008_entryinvoicehandle'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrytype',
            name='price',
            field=models.DecimalField(default=0, verbose_name='price', max_digits=9, decimal_places=2),
            preserve_default=False,
        ),
    ]
