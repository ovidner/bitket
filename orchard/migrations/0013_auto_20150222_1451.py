# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0012_auto_20150215_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orchestramemberregistration',
            name='purchase',
            field=models.OneToOneField(related_name='orchestra_member_registration', verbose_name='purchase', to='tickle.Purchase'),
            preserve_default=True,
        ),
    ]
