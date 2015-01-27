# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_default_data(apps, schema_editor):
    EntryType = apps.get_model('karthago', 'EntryType')
    MaterialRole = apps.get_model('karthago', 'MaterialRole')

    EntryType.objects.create(name='Fribygge', description='Max 10 personer, 3000 kr', max_members=10)
    EntryType.objects.create(name='Mikrobygge', description='Max 10 personer, 3500 kr', max_members=10)
    EntryType.objects.create(name='Makrobygge', description='Max 25 personer, 4500 kr', max_members=10)

    MaterialRole.objects.create(name=u'Bärande')
    MaterialRole.objects.create(name=u'Dekorativt')


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_data)
    ]
