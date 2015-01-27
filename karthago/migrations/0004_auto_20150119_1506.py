# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0003_auto_20150118_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrycustommaterial',
            options={'verbose_name': 'entry custom material', 'verbose_name_plural': 'entry custom materials'},
        ),
        migrations.AlterModelOptions(
            name='entrymaterial',
            options={'ordering': ('entry', 'material', 'role'), 'verbose_name': 'entry material', 'verbose_name_plural': 'entry materials'},
        ),
        migrations.AlterModelOptions(
            name='entrytype',
            options={'ordering': ('max_members', 'name'), 'verbose_name': 'entry type', 'verbose_name_plural': 'entry types'},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ('-name',), 'verbose_name': 'material', 'verbose_name_plural': 'materials'},
        ),
        migrations.AlterModelOptions(
            name='materialrole',
            options={'verbose_name': 'material role', 'verbose_name_plural': 'material roles'},
        ),
    ]
