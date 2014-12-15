# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickleuser',
            name='person',
            field=models.OneToOneField(related_name='user', null=True, blank=True, to='tickle.Person'),
            preserve_default=True,
        ),
    ]
