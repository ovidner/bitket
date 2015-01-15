# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_default_data(apps, schema_editor):
    EntryType = apps.get_model('karthago', 'EntryType')

    EntryType.objects.create(name='Fribygge', description='Max 10 personer, 3000 kr', max_members=10)


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_data)
    ]
