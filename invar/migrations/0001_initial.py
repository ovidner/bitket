# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import invar.models


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0017_holding_invalidated'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoldingInvoiceRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('holding', models.ForeignKey(related_name='holding_invoice_rows', verbose_name='holding', to='tickle.Holding')),
            ],
            options={
                'verbose_name': 'holding invoice row',
                'verbose_name_plural': 'holding invoice rows',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('receiver_name', models.CharField(max_length=255, verbose_name='receiver name', blank=True)),
                ('receiver_organisation', models.CharField(max_length=255, verbose_name='receiver organisation', blank=True)),
                ('receiver_pid', models.CharField(max_length=11, verbose_name='receiver PID', blank=True)),
                ('receiver_email', models.EmailField(max_length=254, verbose_name='receiver email address')),
                ('issue_date', models.DateField(default=invar.models.default_invoice_issue_date, null=True, verbose_name='issue date', blank=True)),
                ('due_date', models.DateField(default=invar.models.default_invoice_due_date, null=True, verbose_name='due date', blank=True)),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'invoice',
                'verbose_name_plural': 'invoices',
            },
        ),
        migrations.CreateModel(
            name='InvoiceHandle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice', models.OneToOneField(related_name='handle', verbose_name='invoice', to='invar.Invoice')),
            ],
            options={
                'verbose_name': 'invoice handle',
                'verbose_name_plural': 'invoice handles',
            },
        ),
        migrations.CreateModel(
            name='InvoiceInvalidation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('invoice', models.OneToOneField(related_name='invalidation', verbose_name='invoice', to='invar.Invoice')),
                ('replacement', models.OneToOneField(related_name='replacing_invalidation', verbose_name='replacement invoice', to='invar.Invoice')),
            ],
            options={
                'verbose_name': 'invoice invalidation',
                'verbose_name_plural': 'invoice invalidations',
            },
        ),
        migrations.CreateModel(
            name='InvoiceRow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('person', models.CharField(max_length=256, verbose_name='person', blank=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('price', models.DecimalField(verbose_name='price', max_digits=9, decimal_places=2)),
                ('invoice', models.ForeignKey(related_name='rows', verbose_name='invoice', to='invar.Invoice')),
            ],
            options={
                'verbose_name': 'invoice row',
                'verbose_name_plural': 'invoice rows',
            },
        ),
        migrations.CreateModel(
            name='PersonInvoiceHandle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handle', models.OneToOneField(related_name='person_handle', verbose_name='handle', to='invar.InvoiceHandle')),
                ('person', models.ForeignKey(related_name='invoice_handles', verbose_name='person', to='tickle.Person')),
            ],
            options={
                'verbose_name': 'personal invoice handle',
                'verbose_name_plural': 'personal invoice handles',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('amount', models.DecimalField(verbose_name='amount', max_digits=9, decimal_places=2)),
                ('reference', models.CharField(max_length=256, verbose_name='reference')),
            ],
            options={
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
            },
        ),
        migrations.CreateModel(
            name='TransactionMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handle', models.ForeignKey(related_name='transaction_matches', verbose_name='invoice handle', to='invar.InvoiceHandle')),
                ('transaction', models.OneToOneField(related_name='match', verbose_name='transaction', to='invar.Transaction')),
            ],
            options={
                'verbose_name': 'transaction match',
                'verbose_name_plural': 'transaction matches',
            },
        ),
        migrations.AddField(
            model_name='holdinginvoicerow',
            name='invoice_row',
            field=models.OneToOneField(related_name='holding_row', verbose_name='invoice row', to='invar.InvoiceRow'),
        ),
    ]
