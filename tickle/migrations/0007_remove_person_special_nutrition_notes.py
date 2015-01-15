# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0006_person_special_nutrition_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='special_nutrition_notes',
        ),
    ]
