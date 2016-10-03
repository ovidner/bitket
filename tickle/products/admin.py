from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import Product, Holding, Cart, ProductVariation, ProductVariationChoice
from tickle.modifiers.admin import ModifierInline


class ProductVariationChoiceInline(admin.TabularInline):
    model = ProductVariationChoice


class CartAdmin(admin.ModelAdmin):
    pass


class HoldingAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class ProductVariationAdmin(admin.ModelAdmin):
    inlines = [ProductVariationChoiceInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
