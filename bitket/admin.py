from django.contrib import admin

from . import models


@admin.register(models.AccessCode)
class AccessCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StudentUnionMemberCondition)
class StudentUnionMemberConditionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    pass


class ModifierInline(admin.TabularInline):
    model = models.Modifier


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    filter_horizontal = ['admins']


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'created']
    date_hierarchy = 'created'


class VariationChoiceInline(admin.TabularInline):
    model = models.VariationChoice


class TicketOwnershipInline(admin.TabularInline):
    model = models.TicketOwnership
    raw_id_fields = ['user', 'transactions']
    extra = 0


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_type', 'created', 'utilized', 'current_owner', 'variation_choices']
    list_filter = ['ticket_type__event', 'ticket_type', 'variation_choices']
    search_fields = ['ownerships__user__name', 'ownerships__user__email']
    inlines = [TicketOwnershipInline]
    raw_id_fields = ['access_code']
    ordering = ['-created']

    def current_owner(self, obj):
        return obj.ownerships.latest().user


@admin.register(models.TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    inlines = [ModifierInline]


@admin.register(models.Variation)
class VariationAdmin(admin.ModelAdmin):
    inlines = [VariationChoiceInline]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    list_filter = ['student_union', 'is_staff', 'is_superuser']
    search_fields = ['name', 'email']
