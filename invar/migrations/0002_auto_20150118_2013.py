# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='create_date',
            field=models.DateField(default=datetime.date(2015, 1, 18), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.date(2015, 2, 1)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customerEmail',
            field=models.EmailField(max_length=254),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customerFirstname',
            field=models.CharField(max_length=255, verbose_name=b'F\xc3\xb6rnamn'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customerLastname',
            field=models.CharField(max_length=255, verbose_name=b'Efternamn'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customerOrganization',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'F\xc3\xb6rening'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.IntegerField(unique=True),
            preserve_default=True,
        ),
    ]
