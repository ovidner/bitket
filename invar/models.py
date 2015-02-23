# -*- coding: utf-8 -*-
from django.db import models
import datetime
from random import randint


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


def generate_invoice(name, email, orgName, id_nr, stuff):
    bill = Invoice(customerName=name,
                   customerOrganization=orgName,
                   customerPNR=id_nr,
                   customerEmail=email,
                   invoice_number=randint(0, 1000000))
    bill.save()

    for thing in stuff:
        row = InvoiceRow(invoice=bill, itemName=thing[0].name, nrItems=thing[1], itemCost=thing[0].price)
        row.save()
