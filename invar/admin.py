# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from invar.models import Invoice, InvoiceRow, Transaction, TransactionMatch, InvoiceHandle, InvoiceInvalidation, HoldingInvoiceRow, PersonInvoiceHandle


class HoldingInvoiceRowInline(admin.TabularInline):
    model = HoldingInvoiceRow
    raw_id_fields = ('holding',)


@admin.register(InvoiceRow)
class InvoiceRowAdmin(admin.ModelAdmin):
    inlines = (HoldingInvoiceRowInline,)


class InvoiceRowInline(admin.TabularInline):
    model = InvoiceRow
    extra = 0
    readonly_fields = ('pk',)


class InvoiceHandleInline(admin.TabularInline):
    model = InvoiceHandle
    extra = 0
    max_num = 1

    readonly_fields = ('ocr',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', )

    inlines = (InvoiceHandleInline, InvoiceRowInline, )


@admin.register(InvoiceInvalidation)
class InvoiceInvalidationAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(TransactionMatch)
class TransactionMatchAdmin(admin.ModelAdmin):
    pass
