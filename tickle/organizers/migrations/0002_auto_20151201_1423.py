# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='slug',
            field=tickle.common.db.fields.SlugField(editable=False, populate_from='name', max_length=64, unique=True, verbose_name='slug'),
        ),
    ]
