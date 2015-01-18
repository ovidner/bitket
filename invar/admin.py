from django.contrib import admin
from Invar.models import Invoice, InvoiceRow

# Register your models here.

@admin.register(Invoice)
class InvoiceAdmin(admin.modelAdmin):
    pass