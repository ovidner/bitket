# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0001_initial'),
        ('tickle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orchestramember',
            name='person',
            field=models.OneToOneField(related_name='orchestra_member', to='tickle.Person'),
            preserve_default=True,
        ),
    ]
