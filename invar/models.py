# -*- coding: utf-8 -*-
from django.db import models
import django.utils.timezone
import datetime
from random import randint
from tickle.models.products import Holding
from enumfields import EnumField
from enum import Enum
import tickle.utils.mail as mail


def get_new_invoice_id():
    return randint(0, 1000000)


class Invoice(models.Model):
    class OrderStatus(Enum):
        GENERATED = 'g'
        SENT = 's'
        PAYED = 'p'
        #makulerad!
        OBLITERATED = 'o'
        LATE = 'L'

    invoice_number = models.IntegerField(unique=True, verbose_name='Fakturanummer')
    customerName = models.CharField(max_length=255, verbose_name='Namn', default='')
    customerOrganization = models.CharField(max_length=255, default='', verbose_name='Förening')
    customerPNR = models.CharField(max_length=10, verbose_name='Personnummer')
    customerEmail = models.EmailField(max_length=254, verbose_name='mail')
    create_date = models.DateField(auto_now_add=True, default=datetime.date.today())
    sent_date = models.DateField(null=True)
    due_date = models.DateField(default=datetime.date.today() + datetime.timedelta(days=21))
    current_status = EnumField(OrderStatus, max_length=1, default='g')

    def send_invoice(self):
        self.sent_date = django.utils.timezone.now()
        self.current_status = 'S'
        self.save()
        self.send_invoice_mail()

    def send_invoice_mail(self):
        #make data dict
        invoice_data = self.get_invoice_data()
        mail.TemplatedEmail(subject='SOF15 faktura', body_template_html='invar/email/invoice.html',
                            context=invoice_data, from_email="sof15MONEHS@sof.se", to=self.customerEmail)

    def get_invoice_data(self):
        data = dict()
        data['customerName'] = self.customerName
        data['customerOrganization'] = self.customerOrganization
        data['customerPNR'] = self.customerPNR
        data['sentDate'] = self.sent_date
        data['dueDate'] = self.due_date
        #retrive the invoice rows

        products_summary = dict()
        products_specification = list()

        for row in self.rows.all():
            products_specification.append(row.get_details())
            if row.itemName in products_summary:
                products_summary[row.itemName] += row.nrItems
            else:
                products_summary[row.itemName] = row.nrItems



class InvoiceRow(models.Model):
    invoice = models.ForeignKey(Invoice,related_name='rows')
    itemName = models.CharField(max_length=255, verbose_name='Pryl')
    nrItems = models.IntegerField(default=1, verbose_name='Antal')
    itemCost = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Pris')
    holdingBackref = models.ForeignKey(Holding, null=True)

    def get_details(self):
        details = dict()
        if self.holdingBackref:
            details['ownerId'] = self.holdingBackref.person.pk
            details['ownerName'] = self.holdingBackref.person.full_name

        details['itemName'] = self.itemName
        details['nItems'] = self.nrItems
        details['itemCost'] = self.itemCost
        return details




def generate_invoice(name, email, orgName, id_nr, stuff):
    bill = Invoice(customerName=name,
                   customerOrganization=orgName,
                   customerPNR=id_nr,
                   customerEmail=email,
                   invoice_number=get_new_invoice_id(),
                   )
    bill.save()

    for thing in stuff:
        row = InvoiceRow(invoice=bill, itemName=thing[0].name, nrItems=thing[1],
                         itemCost=thing[0].price, holdingBackref=thing[2])
        row.save()
