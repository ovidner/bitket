# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.helpers import ActionForm
from django import forms
from django.template.response import TemplateResponse

from invar.models import Invoice, InvoiceRow, Transaction, TransactionMatch, InvoiceHandle, InvoiceInvalidation, HoldingInvoiceRow
from tickle.admin import AlwaysChangedModelForm
from invar.views import BgMaxImportView
from invar.forms import EmailInvoiceForm

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
    form = AlwaysChangedModelForm
    extra = 0
    max_num = 1

    readonly_fields = ('ocr',)


class InvoiceStatusFilter(admin.SimpleListFilter):
    title = _('status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ['current', _('Current')],
            ['invalidated', _('Invalidated')],
            ['replaced', _('Replaced')]
        ]

    def queryset(self, request, queryset):
        if self.value() == 'current':
            return queryset.current()
        elif self.value() == 'invalidated':
            return queryset.invalidated()
        elif self.value() == 'replaced':
            return queryset.replaced()


class InvoicePaymentStatusFilter(admin.SimpleListFilter):
    title = _('payment status')
    parameter_name = 'payment_status'

    def lookups(self, request, model_admin):
        return [
            ['pending', _('Pending')],
            ['payed', _('Payed')],
            ['overdue', _('Overdue')],
            ['overpayed', _('Overpayed')],
        ]

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.pending()
        elif self.value() == 'payed':
            return queryset.payed()
        elif self.value() == 'overdue':
            return queryset.overdue()
        elif self.value() == 'overpayed':
            return queryset.overpayed()


class InvoiceActionForm(ActionForm):
    email = forms.EmailField(required=False, label='email')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'receiver_name', 'due_date', 'total', 'payed', 'status_render', 'payment_status_render')
    list_display_links = ('id', 'receiver_name')
    list_filter = [InvoiceStatusFilter, InvoicePaymentStatusFilter]

    inlines = (InvoiceHandleInline, InvoiceRowInline)

    def status_render(self, obj):
        status = obj.status

        if status == 'current':
            return _('Current')
        elif status == 'invalidated':
            return _('Invalidated')
        elif status == 'replaced':
            return _('Replaced')

    def payment_status_render(self, obj):
        status = obj.payment_status

        if status == 'payed':
            return _('Payed')
        elif status == 'overpayed':
            return _('Overpayed')
        elif status == 'pending':
            return _('Pending')
        elif status == 'overdue':
            return _('Overdue')

    search_fields = ('id', )

    actions = ['send_invoice', 'mail_invoice', ]

    def send_invoice(self, request, queryset):
        for invoice in queryset:
            invoice.send()
        self.message_user(request, _('Invoice sent.'))

    send_invoice.short_description = _('Resend invoice (Used for lost invoices).')

    def mail_invoice(self, request, queryset):
        if request.POST.get('post'):
            form = EmailInvoiceForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                for invoice in queryset:
                    invoice.send(email=email)
                self.message_user(request, _('Invoices sent to %s.') % email)
                return
        else:
            form = EmailInvoiceForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        context = {
            'objects': queryset,
            'form': form
        }
        return TemplateResponse(request, 'admin/invar/email_invoice.html', context)

    mail_invoice.short_description = _('Email invoices')


@admin.register(InvoiceInvalidation)
class InvoiceInvalidationAdmin(admin.ModelAdmin):
    pass


class TransactionMatchInline(admin.TabularInline):
    model = TransactionMatch
    extra = 0
    max_num = 1
    raw_id_fields = ('handle',)


class TransactionMatchedListFilter(admin.SimpleListFilter):
    title = _('matched')

    parameter_name = 'matched'

    def lookups(self, request, model_admin):
        return (
            ('y', _('Yes')),
            ('n', _('No'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'y':
            return queryset.filter(match__isnull=False)
        elif self.value() == 'n':
            return queryset.filter(match__isnull=True)
        return queryset


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'reference', 'timestamp', 'uid')
    list_filter = (TransactionMatchedListFilter,)
    date_hierarchy = 'timestamp'

    actions = ('match_ocr_action',)

    inlines = (TransactionMatchInline,)

    def get_urls(self):
        from django.conf.urls import url

        urls = super(TransactionAdmin, self).get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        custom_urls = [
            url(r'^import/bgmax/$', BgMaxImportView.as_view(template_name='admin/invar/transaction/import_bgmax.html'),
                name='%s_%s_import_bgmax' % info),
        ]

        return custom_urls + urls  # Add our own first so the pk filter won't catch them

    def match_ocr_action(self, request, queryset):
        queryset.match_ocr()

        self.message_user(request, _('Successfully matched by OCR.'))

    match_ocr_action.short_description = _('Match by OCR')
