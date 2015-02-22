from django.contrib import admin
from django.db import models
from invar.models import Invoice, InvoiceRow
from django.forms import TextInput
from django.conf.urls import patterns, url
from functools import update_wrapper

# Register your models here.

class InvoiceRowInline(admin.TabularInline):
    model = InvoiceRow
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceRowInline, )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 20})}
    }

    def generate_invoice_view(self, request, extra_content=None):
        return "Hello world"
