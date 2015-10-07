# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, help_text='Determines whether the condition should be displayed and included in queries.', verbose_name='active')),
            ],
            options={
                'verbose_name': 'condition',
                'verbose_name_plural': 'conditions',
            },
        ),
        migrations.CreateModel(
            name='StudentUnionMemberCondition',
            fields=[
                ('condition_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='conditions.Condition')),
            ],
            options={
                'verbose_name': 'student union member condition',
                'verbose_name_plural': 'student union member conditions',
            },
            bases=('conditions.condition',),
        ),
    ]
