# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0008_auto_20150130_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='holdings',
        ),
        migrations.AddField(
            model_name='holding',
            name='purchase',
            field=models.ForeignKey(related_name='holdings', verbose_name='purchase', blank=True, to='tickle.Purchase', null=True),
            preserve_default=True,
        ),
    ]
