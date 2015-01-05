from django.contrib import admin

from .models import *


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass


@admin.register(EntryMaterial)
class EntryMaterialAdmin(admin.ModelAdmin):
    pass

@admin.register(EntryCustomMaterial)
class EntryCustomMaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(EntryType)
class EntryTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(MaterialRole)
class MaterialRoleAdmin(admin.ModelAdmin):
    pass