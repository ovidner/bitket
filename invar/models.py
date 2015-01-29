# -*- coding: utf-8 -*-
from django.db import models
import datetime


class Invoice(models.Model):
    invoice_number = models.IntegerField(unique=True, verbose_name='Fakturanummer')
    customerName = models.CharField(max_length=255, verbose_name='Namn', default='')
    customerOrganization = models.CharField(max_length=255, default='', verbose_name='Förening')
    customerPNR = models.CharField(max_length=10, verbose_name='Personnummer')
    customerEmail = models.EmailField(max_length=254, verbose_name='mail')
    create_date = models.DateField(auto_now_add=True, default=datetime.date.today())
    due_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=14))


class InvoiceRow(models.Model):
    invoice = models.ForeignKey(Invoice)
    itemName = models.CharField(max_length=255, verbose_name='Pryl')
    nrItems = models.IntegerField(default=1, verbose_name='Antal')
    itemCost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Pris')