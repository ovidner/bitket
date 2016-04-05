from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import StudentUnionMemberCondition


class StudentUnionMemberConditionAdmin(admin.ModelAdmin):
    pass


admin.site.register(StudentUnionMemberCondition, StudentUnionMemberConditionAdmin)
