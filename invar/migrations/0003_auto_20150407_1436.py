# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import invar.models


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0002_auto_20150323_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='create_date',
            field=models.DateField(default=invar.models.default_invoice_creation_date),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=invar.models.default_invoice_due_date),
        ),
    ]
