# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conditions', '0001_initial'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentunionmembercondition',
            name='student_union',
            field=models.ForeignKey(related_name='+', verbose_name='student union', to='people.StudentUnion'),
        ),
    ]
