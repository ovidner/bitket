from django.contrib import admin

from .models import *


class EntryMaterialInlineAdmin(admin.TabularInline):
    model = EntryMaterial


class EntryCustomMaterialInlineAdmin(admin.TabularInline):
    model = EntryCustomMaterial


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    inlines = (EntryMaterialInlineAdmin, EntryCustomMaterialInlineAdmin)


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
    list_display = ['name', 'total_amount', 'unit']


@admin.register(MaterialRole)
class MaterialRoleAdmin(admin.ModelAdmin):
    pass