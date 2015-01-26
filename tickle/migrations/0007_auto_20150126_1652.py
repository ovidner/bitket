# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0006_auto_20150121_2108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'person', 'verbose_name_plural': 'people', 'permissions': (('view_person', 'Can view person'),)},
        ),
        migrations.AlterField(
            model_name='tickleuser',
            name='username',
            field=models.CharField(unique=True, max_length=256, verbose_name='LiU-ID or email address'),
            preserve_default=True,
        ),
    ]
