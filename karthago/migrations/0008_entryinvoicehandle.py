# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0001_initial'),
        ('karthago', '0007_auto_20150509_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryInvoiceHandle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry', models.ForeignKey(related_name='invoice_handles', verbose_name='entry', to='karthago.Entry')),
                ('handle', models.OneToOneField(related_name='kartege_entry_handle', verbose_name='handle', to='invar.InvoiceHandle')),
            ],
            options={
                'verbose_name': 'K\xe5rtege entry invoice handle',
                'verbose_name_plural': 'K\xe5rtege entry invoice handles',
            },
        ),
    ]
