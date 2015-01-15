# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0002_purchase_valid'),
        ('orchard', '0002_auto_20150115_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orchestraproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='OrchestraProduct',
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='purchase_object',
            field=models.ForeignKey(to='tickle.Purchase', null=True),
            preserve_default=True,
        ),
    ]
