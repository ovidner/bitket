# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fungus', '0006_functionaryshifttypediscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionarydiscount',
            name='functionary',
            field=models.BooleanField(default=True, verbose_name='must be functionary'),
        ),
    ]
