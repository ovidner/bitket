# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0008_auto_20150115_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holding',
            name='person',
            field=models.ForeignKey(related_name='holdings', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='holding',
            name='product',
            field=models.ForeignKey(related_name='holdings', to='tickle.Product'),
            preserve_default=True,
        ),
    ]
