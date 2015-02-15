# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0009_auto_20150215_2009'),
        ('orchard', '0011_auto_20150129_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orchestra',
            name='contactEmail',
        ),
        migrations.RemoveField(
            model_name='orchestra',
            name='contactName',
        ),
        migrations.RemoveField(
            model_name='orchestra',
            name='orgNr',
        ),
        migrations.AddField(
            model_name='orchestra',
            name='contact',
            field=models.ForeignKey(related_name='orchestra_contacts', blank=True, editable=False, to='tickle.Person', null=True, verbose_name='contact'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestra',
            name='organisation_number',
            field=models.CharField(default='', max_length=11, verbose_name='organisation number', blank=True),
            preserve_default=True,
        ),
    ]
