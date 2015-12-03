# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20151125_0231'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='liu_student_union',
            new_name='student_union',
        ),
        migrations.AlterField(
            model_name='studentunion',
            name='slug',
            field=tickle.common.db.fields.SlugField(editable=False, populate_from='name', max_length=64, unique=True, verbose_name='slug'),
        ),
    ]
