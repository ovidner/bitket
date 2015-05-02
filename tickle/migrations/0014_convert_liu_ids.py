# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def convert_empty_string_liu_ids_to_null(apps, schema_editor):
    Person = apps.get_model('tickle', 'Person')

    Person.objects.filter(liu_id='').update(liu_id=None)


def convert_empty_string_liu_ids_to_null_reverse(apps, schema_editor):
    Person = apps.get_model('tickle', 'Person')

    Person.objects.filter(liu_id=None).update(liu_id='')


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0013_auto_20150502_1441'),
    ]

    operations = [
        migrations.RunPython(
            convert_empty_string_liu_ids_to_null,
            convert_empty_string_liu_ids_to_null_reverse
        )
    ]
