# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Permission

from gfklookupwidget.widgets import GfkLookupWidget
from guardian.models import UserObjectPermission, GroupObjectPermission
from guardian.admin import UserObjectPermissionsForm

from tickle.models import Person, Event, Product, Holding, TicketType, Delivery, Purchase, SpecialNutrition, TickleUser, StudentUnionDiscount, ProductDiscount


class PurchaseInline(admin.StackedInline):
    model = Purchase
    # filter_horizontal = ('holdings',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


class ProductDiscountInline(admin.TabularInline):
    model = ProductDiscount

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'discount_object_id':
            kwargs['widget'] = GfkLookupWidget(
                content_type_field_name='discount_content_type',
                parent_field=ProductDiscount._meta.get_field('discount_content_type'),
                )

        return super(ProductDiscountInline, self).formfield_for_dbfield(db_field, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductDiscountInline,)


@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    pass


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    pass


class HoldingInline(admin.TabularInline):
    model = Holding
    raw_id_fields = ('person',)
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = (HoldingInline,)
    list_display = ('person', 'purchased')


@admin.register(SpecialNutrition)
class SpecialNutritionAdmin(admin.ModelAdmin):
    pass


class TickleUserAdminForm(forms.ModelForm):
    class Meta:
        model = TickleUser
        fields = ('person', 'is_active', 'is_admin')


@admin.register(TickleUser)
class TickleUserAdmin(UserAdmin):
    form = TickleUserAdminForm
    add_form = TickleUserAdminForm
    fieldsets = (
        (None, {'fields': ('person', )}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Stuff', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('person', )}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Stuff', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
    )

    list_display = ('person', 'is_active', 'is_admin')
    list_filter = ('is_admin', 'is_superuser', 'is_active', 'groups')
    raw_id_fields = ('person',)


class AlwaysChangedModelForm(forms.ModelForm):
    def has_changed(self):
        return True


class TickleUserInline(admin.StackedInline):
    model = TickleUser
    form = AlwaysChangedModelForm  # This way we can just press Add, not change anything and still get an account created
    extra = 0
    max_num = 1

    exclude = ('username', 'password',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (TickleUserInline, PurchaseInline,)

    list_display = ('first_name', 'last_name', 'pid', 'email', 'phone', 'liu_id')
    list_display_links = ('first_name', 'last_name', 'pid')
    list_filter = ('special_nutrition',)

    search_fields = ('first_name', 'last_name', 'email', 'liu_id__liu_id')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserObjectPermission)
class UserObjectPermissionAdmin(admin.ModelAdmin):
    search_fields = (
        'user__person__first_name',
        'user__person__last_name',
        'user__person__email',
        'permission__name',
        'permission__codename'
    )
    list_filter = ('content_type',)


@admin.register(GroupObjectPermission)
class GroupObjectPermissionAdmin(admin.ModelAdmin):
    search_fields = (
        'group__name',
        'permission__name',
        'permission__codename'
    )
    list_filter = ('content_type',)


@admin.register(StudentUnionDiscount)
class StudentUnionDiscountAdmin(admin.ModelAdmin):
    pass
