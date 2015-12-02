# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainevent',
            name='slug',
            field=tickle.common.db.fields.SlugField(populate_from=b'name', unique_with=(b'organizer__slug',), editable=True, max_length=64, verbose_name='slug'),
        ),
    ]
