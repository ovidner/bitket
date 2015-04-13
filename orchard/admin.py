# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponse, HttpResponseRedirect

from guardian.admin import GuardedModelAdmin

from tickle.models import Product
from tickle.admin import PersonAdmin
from orchard.models import OrchardPerson, Orchestra, OrchestraMembership, OrchestraTicketType, OrchestraProduct, \
    OrchestraMemberRegistration


class ProductFilter(admin.SimpleListFilter):
    title = _('holds product')
    parameter_name = 'product'

    def lookups(self, request, model_admin):
        products = set([i for i in Product.objects.all()])
        return [(i.pk, i.name) for i in products]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(holdings__product=self.value())
        else:
            return queryset


@admin.register(OrchardPerson)
class OrchardPersonAdmin(PersonAdmin):
    actions = ('csv_export',)
    list_display = ('first_name', 'last_name', 'pid', 'email', 'phone', 'primary_orchestra', 'notes')
    list_filter = ('orchestra_memberships__orchestra', 'special_nutrition', ProductFilter)

    def has_add_permission(self, request):
        # We should not add people from here.
        return False

    def get_queryset(self, request):
        return OrchardPerson.objects.exclude(orchestra_memberships__isnull=True)

    def csv_export(self, request, queryset):
        import unicodecsv

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orchestra-members.csv"'

        writer = unicodecsv.writer(response, delimiter=b';')

        # We can't use lazy translation here.
        writer.writerow(
            (ugettext('Name'), ugettext('PID'), ugettext('Primary orchestra'), ugettext('Other orchestras')))
        for p in queryset.select_related('orchestra_memberships'):
            writer.writerow(
                [p.full_name, p.pid] + [i.orchestra.name for i in p.orchestra_memberships.order_by('-primary')])

        return response

    csv_export.short_description = _('Export selected objects as CSV file')

    def primary_orchestra(self, obj):
        return obj.primary_orchestra.name


@admin.register(OrchestraMembership)
class OrchestraMembershipAdmin(admin.ModelAdmin):
    list_display = ('person', 'orchestra', 'primary', 'approved')
    list_filter = ('orchestra', 'primary', 'approved')


class OrchestraMembershipInline(admin.TabularInline):
    model = OrchestraMembership
    extra = 0


@admin.register(Orchestra)
class OrchestraAdmin(admin.ModelAdmin):
    actions = ['generate_invoice']
    inlines = (OrchestraMembershipInline,)

    def generate_invoice(self, request, queryset):
        queryset.invoice()

    generate_invoice.short_description = _('Invoice orchestra')


@admin.register(OrchestraTicketType)
class OrchestraTicketTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(OrchestraProduct)
class OrchestraProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'invoicable_quantity')

    def invoicable_quantity(self, obj):
        return obj.holdings.filter(purchase__person__orchestra_memberships__approved=True,
                                   purchase__person__orchestra_memberships__primary=True).distinct().quantity()

    invoicable_quantity.short_description = _('invoicable quantity')


@admin.register(OrchestraMemberRegistration)
class OrchestraMemberRegistrationAdmin(admin.ModelAdmin):
    list_display = ('person',)
    raw_id_fields = ('purchase',)

    def person(self, obj):
        return obj.purchase.person
