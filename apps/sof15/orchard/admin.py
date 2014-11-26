from django.contrib import admin

from orchard.models import Orchestra, OrchestraMember

@admin.register(Orchestra)
class OrchestraAdmin(admin.ModelAdmin):
    pass

@admin.register(OrchestraMember)
class OrchestraMemberAdmin(admin.ModelAdmin):
    pass