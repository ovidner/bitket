from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import MainEvent


class MainEventAdmin(admin.ModelAdmin):
    pass


admin.site.register(MainEvent, MainEventAdmin)
