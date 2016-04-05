from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import HoldingModifier, ProductModifier


class HoldingModifierInline(admin.TabularInline):
    model = HoldingModifier


class ProductModifierInline(admin.TabularInline):
    model = ProductModifier
