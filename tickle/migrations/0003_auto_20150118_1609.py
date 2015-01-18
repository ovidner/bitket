# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0002_auto_20150118_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickettype',
            name='id',
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='product',
            field=models.OneToOneField(parent_link=True, related_name='ticket_type', primary_key=True, serialize=False, to='tickle.Product'),
            preserve_default=True,
        ),
    ]
