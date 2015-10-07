# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0003_auto_20150323_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='primary_contact_email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='secondary_contact_email',
            field=models.EmailField(max_length=254, verbose_name='email'),
        ),
    ]
