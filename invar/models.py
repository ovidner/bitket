# -*- coding: utf-8 -*-
from django.db import models


class Invoice(models.Model):
    invoice_number = models.IntegerField()
    customerFirstname = models.CharField(max_length=255)
    customerLastname = models.CharField(max_length=255)
    customerOrganization = models.CharField(max_length=255, default='')
    customerPNR = models.CharField(max_length=10)
    customerEmail = models.CharField(max_length=255)


class InvoiceRow(models.Model):
    invoice = models.ForeignKey('Invoice')
    itemCost = models.DecimalField(max_digits=9, decimal_places=2)
    nrItems = models.IntegerField(default=1)
    itemName = models.CharField(max_length=255)