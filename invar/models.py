# -*- coding: utf-8 -*-
from django.db import models
import django.utils.timezone
import datetime
from random import randint
from tickle.models.products import Holding
from enumfields import EnumField
from enum import Enum
import tickle.utils.mail as mail

class Invoice(models.Model):
    class OrderStatus(Enum):
        GENERATED = 'g'
        SENT = 's'
        PAYED = 'p'
        #makulerad!
        OBLITERATED = 'o'
        LATE = 'L'

    invoice_number = models.IntegerField(unique=True, verbose_name='Fakturanummer', null=True)
    customer_name = models.CharField(max_length=255, verbose_name='Namn', default='')
    customer_organization = models.CharField(max_length=255, default='', verbose_name='Förening')
    customer_PNR = models.CharField(max_length=10, verbose_name='Personnummer')
    customer_mail = models.EmailField(max_length=254, verbose_name='mail')
    create_date = models.DateField(auto_now_add=True, default=django.utils.timezone.now())
    sent_date = models.DateField(null=True)
    due_date = models.DateField(default=None, nullable=True)
    current_status = EnumField(OrderStatus, max_length=1, default='g')
    invoice_ocr = models.CharField(max_length=255, unique=True, verbose_name='OCR')

    def send_invoice(self):
        self.sent_date = django.utils.timezone.now()
        self.due_date = django.utils.timezone.now() + django.utils.timezone.timedelta(days=14)
        self.current_status = self.OrderStatus.SENT
        self.save()
        self.send_invoice_mail()

    def send_invoice_mail(self):
        #make data dict
        invoice_data = self.get_invoice_data()
        mail.TemplatedEmail(subject='SOF15 faktura', body_template_html='invar/email/invoice.html',
                            context=invoice_data, from_email="sof15MONEHS@sof.se", to=self.customerEmail)

    def get_invoice_data(self):
        data = dict()
        data['customer_name'] = self.customer_name
        data['customer_organization'] = self.customer_organization
        data['customer_PNR'] = self.customerPNR
        data['sent_date'] = self.sent_date
        data['due_date'] = self.due_date
        data['invoice_number'] = self.invoice_number
        #retrive the invoice rows

        products_specification = list()
        total_sum = 0
        for row in self.rows.all():
            row_details = row.get_details()
            row_details['row_total'] = row_details['item_cost'] * row_details['num_items']
            products_specification.append(row_details)
            total_sum = row_details['item_cost'] * row_details['num_items']


        data['products'] = products_specification
        data['invoice_total'] = total_sum
        return data

    def get_luhn_check(self, invoice_id):
        digits = str(invoice_id)
        sum = 0
        for number in digits:
            sum = sum + int(number)

        return str(sum*9)[-1]


class InvoiceRow(models.Model):
    invoice = models.ForeignKey(Invoice,related_name='rows')
    itemName = models.CharField(max_length=255, verbose_name='Pryl')
    nrItems = models.IntegerField(default=1, verbose_name='Antal')
    itemCost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Pris')
    holdingBackref = models.ForeignKey(Holding, null=True)

    def get_details(self):
        details = dict()
        if self.holdingBackref:
            details['owner_id'] = self.holdingBackref.person.pk
            details['owner_name'] = self.holdingBackref.person.full_name

        details['item_name'] = self.itemName
        details['num_items'] = self.nrItems
        details['item_cost'] = self.itemCost
        return details


def generate_invoice(name, email, orgName, id_nr, stuff):
    invoice_offset = 100000
    bill = Invoice(customerName=name,
                   customerOrganization=orgName,
                   customerPNR=id_nr,
                   customerEmail=email
                   )
    bill.save()
    bill.invoice_number = bill.pk + invoice_offset
    bill.invoice_ocr = str(bill.invoice_number) + bill.get_luhn_check(bill.invoice_number)
    bill.save()

    for thing in stuff:
        row = InvoiceRow(invoice=bill, itemName=thing[0].name, nrItems=thing[1],
                         itemCost=thing[0].price, holdingBackref=thing[2])
        row.save()

