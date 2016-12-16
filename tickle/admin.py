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


class TicketOwnershipInline(admin.TabularInline):
    model = models.TicketOwnership
    raw_id_fields = ('user', 'transactions',)
    extra = 0


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_type', 'created', 'utilized', 'current_owner')
    list_filter = ('variation_choices',)
    search_fields = ('ownerships__user__name','ownerships__user__email')
    inlines = [TicketOwnershipInline]
    raw_id_fields = ('access_code',)

    def current_owner(self, obj):
        return obj.ownerships.latest().user


@admin.register(models.TicketType)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModifierInline]


@admin.register(models.Variation)
class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [ProductVariationChoiceInline]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass
