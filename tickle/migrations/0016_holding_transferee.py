# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0015_auto_20150507_0527'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='transferee',
            field=models.ForeignKey(related_name='transferee', default=None, blank=True, to='tickle.Person', null=True, verbose_name='transferee'),
        ),
    ]
