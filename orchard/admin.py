# -*- coding: utf-8 -*-
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from orchard.models import Orchestra, OrchestraMembership, OrchestraTicketType
from tickle.models.people import Person
from tickle.models.products import Holding
from invar.models import Invoice, InvoiceRow
from tickle.models.products import Product
from random import randint


def generate_invoice(name, email, orgName, id_nr, stuff):
    bill = Invoice(customerName=name,
                   customerOrganization=orgName,
                   customerPNR=id_nr,
                   customerEmail=email,
                   invoice_number=randint(0, 1000000))
    bill.save()

    for thing in stuff:
        print(thing[0].name)
        row = InvoiceRow(invoice=bill, itemName=thing[0].name, nrItems=thing[1], itemCost=thing[0].price)
        row.save()


def invoice_orchestra(orch_queryset):
    for orch in orch_queryset:
        members = OrchestraMembership.object.filter(approved=True)
        #get the stuff each member has ordered
        total_stuff = []
        for member in members:
            stuff = Holding.objects.filter(person=member.person)
            for thing in stuff:
                product = thing.product
                #print(product)
                quantity = thing.quantity
                total_stuff.append((product, quantity, Person(member.person)))
                #print(total_stuff)
        generate_invoice(orch.contactName, orch.contactEmail, orch.name, orch.orgNr, total_stuff)






class OrchestraMembershipInline(admin.TabularInline):
    model = OrchestraMembership
    extra = 0


@admin.register(Orchestra)
class OrchestraAdmin(GuardedModelAdmin):
    actions = ['generate_invoice']
    inlines = (OrchestraMembershipInline,)

    def generate_invoice(self, request, queryset):
        invoice_orchestra(queryset)


    generate_invoice.short_description = 'Fakturera orkester'


@admin.register(OrchestraTicketType)
class OrchestraTicketTypeAdmin(admin.ModelAdmin):
    pass