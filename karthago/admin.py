# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Count

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
    list_display = ('constellation', 'name', 'entry_type', 'approved', 'members', 'memberships_count')
    list_editable = ('approved',)
    list_display_links = ('constellation', 'name')

    def get_queryset(self, request):
        return super(EntryAdmin, self).get_queryset(request).annotate(Count('memberships'))

    def memberships_count(self, obj):
        return obj.memberships__count

    memberships_count.short_description = _('registered members')


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
