from django.contrib import admin

from . import models


@admin.register(models.AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StudentUnionMemberCondition)
class StudentUnionMemberConditionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Event)
class MainEventAdmin(admin.ModelAdmin):
    pass


class ProductModifierInline(admin.TabularInline):
    model = models.Modifier


@admin.register(models.Organization)
class OrganizerAdmin(admin.ModelAdmin):
    filter_horizontal = ['admins']


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'created')
    date_hierarchy = 'created'


class ProductVariationChoiceInline(admin.TabularInline):
    model = models.VariationChoice


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TicketType)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModifierInline]


@admin.register(models.Variation)
class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [ProductVariationChoiceInline]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass
