# -*- coding: utf-8 -*-
from django.contrib import admin
from orchard.models import Orchestra, OrchestraMembership, OrchestraTicketType


class OrchestraMembershipInline(admin.TabularInline):
    model = OrchestraMembership
    extra = 0


@admin.register(Orchestra)
class OrchestraAdmin(admin.ModelAdmin):
    inlines = (OrchestraMembershipInline,)


@admin.register(OrchestraTicketType)
class OrchestraTicketTypeAdmin(admin.ModelAdmin):
    pass