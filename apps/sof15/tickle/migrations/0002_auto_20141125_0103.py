# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, to='tickle.Event', null=True),
            preserve_default=True,
        ),
    ]
