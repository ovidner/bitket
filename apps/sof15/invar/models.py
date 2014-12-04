# -*- coding: utf-8 -*-
from django.db import models


class Invoice(models.Model):
    pass


class InvoiceRow(models.Model):
    invoice = models.ForeignKey('Invoice')
    amount = models.DecimalField(max_digits=9, decimal_places=2)


class ProductInvoiceRow(InvoiceRow):
    product = models.ForeignKey('tickle.Product')


class OtherInvoiceRow(InvoiceRow):
    text = models.CharField(max_length=256)


class Transaction(models.Model):
    invoice = models.ForeignKey('Invoice', null=True, blank=True)
    reference = models.CharField(max_length=512)
    amount = models.DecimalField(max_digits=9, decimal_places=2)