# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0002_auto_20150118_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='customerFirstname',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='customerLastname',
        ),
        migrations.AddField(
            model_name='invoice',
            name='customerName',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Namn'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='create_date',
            field=models.DateField(default=datetime.date(2015, 1, 29), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customerEmail',
            field=models.EmailField(max_length=254, verbose_name=b'mail'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customerPNR',
            field=models.CharField(max_length=10, verbose_name=b'Personnummer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.date(2015, 2, 12)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.IntegerField(unique=True, verbose_name=b'Fakturanummer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='itemCost',
            field=models.DecimalField(verbose_name=b'Pris', max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='itemName',
            field=models.CharField(max_length=255, verbose_name=b'Pryl'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoicerow',
            name='nrItems',
            field=models.IntegerField(default=1, verbose_name=b'Antal'),
            preserve_default=True,
        ),
    ]
