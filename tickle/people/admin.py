from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import Person, StudentUnion, SpecialNutrition


class PersonAdmin(admin.ModelAdmin):
    pass


class StudentUnionAdmin(admin.ModelAdmin):
    pass


class SpecialNutritionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, PersonAdmin)
admin.site.register(StudentUnion, StudentUnionAdmin)
admin.site.register(SpecialNutrition, SpecialNutritionAdmin)
