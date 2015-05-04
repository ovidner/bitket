from django.contrib import admin

from .models import *
from tickle.admin import PersonAdmin


class EntryMaterialInlineAdmin(admin.TabularInline):
    model = EntryMaterial


class EntryCustomMaterialInlineAdmin(admin.TabularInline):
    model = EntryCustomMaterial


class EntryMembershipInline(admin.TabularInline):
    model = EntryMembership
    raw_id_fields = ('person',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    inlines = (EntryMaterialInlineAdmin, EntryCustomMaterialInlineAdmin, EntryMembershipInline)
    list_display = ('constellation', 'name', 'entry_type', 'approved', 'members')
    list_editable = ('approved',)
    list_display_links = ('constellation', 'name')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_amount', 'unit']


@admin.register(KartegeMemberDiscount)
class KartegeMemberDiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(KartegeMember)
class KartegeMemberAdmin(PersonAdmin):
    def get_queryset(self, request):
        """
        Returns the original queryset but filters out only registered workers and people with shift registrations
        """
        return super(KartegeMemberAdmin, self).get_queryset(request).kartege_members()
