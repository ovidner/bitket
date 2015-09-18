# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0002_auto_20150625_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='reminder_due_date',
            field=models.DateField(null=True, verbose_name='reminder due date', blank=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='reminder_issue_date',
            field=models.DateField(null=True, verbose_name='reminder issue date', blank=True),
        ),
    ]
