# -*- coding: utf-8 -*-
from django.db import models
from django.utils.timezone import now
import datetime
from random import randint
from tickle.models.products import Holding


def default_invoice_creation_date():
    return now()


def default_invoice_due_date():
    return now() + datetime.timedelta(days=14)


class Invoice(models.Model):
    invoice_number = models.IntegerField(unique=True, verbose_name='Fakturanummer')
    customerName = models.CharField(max_length=255, verbose_name='Namn', default='')
    customerOrganization = models.CharField(max_length=255, default='', verbose_name='Förening')
    customerPNR = models.CharField(max_length=10, verbose_name='Personnummer')
    customerEmail = models.EmailField(max_length=254, verbose_name='mail')
    create_date = models.DateField(default=default_invoice_creation_date)
    due_date = models.DateField(default=default_invoice_due_date)


class InvoiceRow(models.Model):
    invoice = models.ForeignKey(Invoice)
    itemName = models.CharField(max_length=255, verbose_name='Pryl')
    nrItems = models.IntegerField(default=1, verbose_name='Antal')
    itemCost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Pris')
    holdingBackref = models.ForeignKey(Holding, null=True)


def generate_invoice(name, email, orgName, id_nr, stuff):
    bill = Invoice(customerName=name,
                   customerOrganization=orgName,
                   customerPNR=id_nr,
                   customerEmail=email,
                   invoice_number=randint(0, 1000000))
    bill.save()

    for thing in stuff:
        row = InvoiceRow(invoice=bill, itemName=thing[0].name, nrItems=thing[1],
                         itemCost=thing[0].price, holdingBackref=thing[2])
        row.save()
