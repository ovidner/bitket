# -*- coding: utf-8 -*-
from django.contrib import admin

from fungus.models import ShiftType, Shift, ShiftRegistration, Worker


@admin.register(ShiftType)
class ShiftTypeAdmin(admin.ModelAdmin):
    pass


class ShiftRegistrationInline(admin.TabularInline):
    model = ShiftRegistration


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    inlines = (ShiftRegistrationInline,)


@admin.register(ShiftRegistration)
class ShiftRegistrationAdmin(admin.ModelAdmin):
    pass


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    inlines = (ShiftRegistrationInline,)