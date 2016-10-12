from django.contrib import admin

from tickle.models import HoldingModifier, ProductModifier, Transaction, \
    ProductVariationChoice
from . import models


@admin.register(models.StudentUnionMemberCondition)
class StudentUnionMemberConditionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MainEvent)
class MainEventAdmin(admin.ModelAdmin):
    pass


class HoldingModifierInline(admin.TabularInline):
    model = HoldingModifier


class ProductModifierInline(admin.TabularInline):
    model = ProductModifier


@admin.register(models.Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    filter_horizontal = ['admins']


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('amount', 'timestamp')
    date_hierarchy = 'timestamp'


class ProductVariationChoiceInline(admin.TabularInline):
    model = ProductVariationChoice


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Holding)
class HoldingAdmin(admin.ModelAdmin):
    inlines = [HoldingModifierInline]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductModifierInline]


@admin.register(models.ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [ProductVariationChoiceInline]

