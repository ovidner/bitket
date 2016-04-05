from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import Organizer


class OrganizerAdmin(admin.ModelAdmin):
    filter_horizontal = ['admins']


admin.site.register(Organizer, OrganizerAdmin)
