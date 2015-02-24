# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0013_auto_20150222_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orchestra',
            name='contact',
            field=models.ForeignKey(related_name='orchestra_contacts', verbose_name='contact', blank=True, to='tickle.Person', null=True),
            preserve_default=True,
        ),
    ]
