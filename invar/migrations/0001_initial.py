# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_number', models.IntegerField(unique=True, verbose_name=b'Fakturanummer')),
                ('customerName', models.CharField(default=b'', max_length=255, verbose_name=b'Namn')),
                ('customerOrganization', models.CharField(default=b'', max_length=255, verbose_name=b'F\xc3\xb6rening')),
                ('customerPNR', models.CharField(max_length=10, verbose_name=b'Personnummer')),
                ('customerEmail', models.EmailField(max_length=254, verbose_name=b'mail')),
                ('create_date', models.DateField(default=datetime.date(2015, 3, 23), auto_now_add=True)),
                ('due_date', models.DateField(default=datetime.date(2015, 4, 6))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemName', models.CharField(max_length=255, verbose_name=b'Pryl')),
                ('nrItems', models.IntegerField(default=1, verbose_name=b'Antal')),
                ('itemCost', models.DecimalField(verbose_name=b'Pris', max_digits=9, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
