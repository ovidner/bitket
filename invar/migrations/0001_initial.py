# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_number', models.IntegerField()),
                ('customerFirstname', models.CharField(max_length=255)),
                ('customerLastname', models.CharField(max_length=255)),
                ('customerOrganization', models.CharField(default=b'', max_length=255)),
                ('customerPNR', models.CharField(max_length=10)),
                ('customerEmail', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('itemCost', models.DecimalField(max_digits=9, decimal_places=2)),
                ('nrItems', models.IntegerField(default=1)),
                ('itemName', models.CharField(max_length=255)),
                ('invoice', models.ForeignKey(to='invar.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
