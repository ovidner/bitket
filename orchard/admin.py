# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from guardian.admin import GuardedModelAdmin

from orchard.models import Orchestra, OrchestraMembership, OrchestraTicketType


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
