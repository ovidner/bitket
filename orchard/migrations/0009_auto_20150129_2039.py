# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0008_auto_20150126_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='orchestra',
            name='contactEmail',
            field=models.CharField(max_length=256, null=True, verbose_name='contact_email'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestra',
            name='contactName',
            field=models.CharField(max_length=256, null=True, verbose_name='contact_name'),
            preserve_default=True,
        ),
    ]
