# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0004_auto_20150119_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orchestramembership',
            name='person',
            field=models.ForeignKey(related_name='orchestra_memberships', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
    ]
