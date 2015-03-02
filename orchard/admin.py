# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from guardian.admin import GuardedModelAdmin

from orchard.models import Orchestra, OrchestraMembership, OrchestraTicketType, OrchestraProduct


class OrchestraMembershipInline(admin.TabularInline):
    model = OrchestraMembership
    extra = 0


@admin.register(Orchestra)
class OrchestraAdmin(GuardedModelAdmin):
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
        return obj.holdings.filter(purchase__person__orchestra_memberships__approved=True, purchase__person__orchestra_memberships__primary=True).distinct().quantity()

    invoicable_quantity.short_description = _('invoicable quantity')
