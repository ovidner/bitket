# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0010_orchestra_orgnr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orchestra',
            name='orgNr',
            field=models.CharField(default=b'', max_length=256, verbose_name='org_nr'),
            preserve_default=True,
        ),
    ]
