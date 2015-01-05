# -*- coding: utf-8 -*-
from django.contrib import admin
from orchard.models import Orchestra, OrchestraMember, OrchestraMembership


class OrchestraMembersInline(admin.TabularInline):
    model = OrchestraMembership
    extra = 0


@admin.register(Orchestra)
class OrchestraAdmin(admin.ModelAdmin):
    inlines = (OrchestraMembersInline,)


@admin.register(OrchestraMember)
class OrchestraMemberAdmin(admin.ModelAdmin):
    inlines = (OrchestraMembersInline,)
