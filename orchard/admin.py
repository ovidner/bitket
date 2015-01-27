# -*- coding: utf-8 -*-
from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from orchard.models import Orchestra, OrchestraMembership, OrchestraTicketType



class OrchestraMembershipInline(admin.TabularInline):
    model = OrchestraMembership
    extra = 0


@admin.register(Orchestra)
class OrchestraAdmin(GuardedModelAdmin):
    inlines = (OrchestraMembershipInline,)


@admin.register(OrchestraTicketType)
class OrchestraTicketTypeAdmin(admin.ModelAdmin):
    pass