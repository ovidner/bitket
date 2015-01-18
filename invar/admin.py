from django.contrib import admin
from django.db import models
from invar.models import Invoice, InvoiceRow
from django.forms import TextInput

# Register your models here.


class InvoiceRowInline(admin.TabularInline):
    model = InvoiceRow
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceRowInline, )
    formfield_overrides = {
        models.CharField: {'widget' : TextInput(attrs={'size':20} ) }
    }