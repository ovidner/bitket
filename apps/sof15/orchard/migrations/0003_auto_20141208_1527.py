# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0002_orchestramember_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='orchestramembership',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='primary',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramember',
            name='orchestras',
            field=models.ManyToManyField(to='orchard.Orchestra', through='orchard.OrchestraMembership'),
            preserve_default=True,
        ),
    ]
