# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponseRedirect

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
    actions = ['change_pass_action']

    def change_pass_action(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect("shifchange/?ids=%s" % ",".join(selected))
    change_pass_action.short_description = "Byt markerade arbetspass"


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    pass