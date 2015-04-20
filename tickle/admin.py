# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse

from gfklookupwidget.widgets import GfkLookupWidget
from guardian.models import UserObjectPermission, GroupObjectPermission
from guardian.admin import UserObjectPermissionsForm
from suit.admin import SortableTabularInline, SortableModelAdmin

from tickle.models import Person, Event, Product, Holding, TicketType, Delivery, Purchase, SpecialNutrition, \
    TickleUser, StudentUnionDiscount, ProductDiscount, Discount, HoldingDiscount
from tickle.utils.kobra import Unauthorized


class PurchaseInline(admin.StackedInline):
    model = Purchase
    extra = 0
    # filter_horizontal = ('holdings',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


class ProductDiscountInline(SortableTabularInline):
    model = ProductDiscount
    extra = 0
    sortable = 'order'


@admin.register(Product)
class ProductAdmin(SortableModelAdmin):
    list_display = ('name', '_public_name', 'price', 'published', 'quantitative', 'purchased_quantity', 'total_quantity')
    list_editable = ('published',)
    inlines = (ProductDiscountInline,)
    sortable = 'order'

    def purchased_quantity(self, obj):
        return obj.holdings.purchased().quantity()

    purchased_quantity.short_description = _('purchased quantity')

    def total_quantity(self, obj):
        return obj.holdings.quantity()

    total_quantity.short_description = _('total quantity')


class HoldingDiscountInline(SortableTabularInline):
    model = HoldingDiscount
    sortable = 'order'


@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    raw_id_fields = ('person', 'purchase', 'shopping_cart',)
    inlines = (HoldingDiscountInline,)


@admin.register(TicketType)
class TicketTypeAdmin(ProductAdmin):
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
    date_hierarchy = 'purchased'


@admin.register(SpecialNutrition)
class SpecialNutritionAdmin(admin.ModelAdmin):
    pass


class TickleUserAdminForm(forms.ModelForm):
    class Meta:
        model = TickleUser
        fields = ('person', 'is_active', 'is_staff')


@admin.register(TickleUser)
class TickleUserAdmin(UserAdmin):
    form = TickleUserAdminForm
    add_form = TickleUserAdminForm
    fieldsets = (
        (None, {'fields': ('person', )}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Stuff', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('person', )}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Stuff', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    list_display = ('person', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    raw_id_fields = ('person',)
    ordering = None  # Parent class uses 'username'


class AlwaysChangedModelForm(forms.ModelForm):
    def has_changed(self):
        return True


class TickleUserInline(admin.StackedInline):
    model = TickleUser
    form = AlwaysChangedModelForm  # This way we can just press Add, not change anything and still get an account
    # created
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ('is_active', 'is_staff')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions', 'is_superuser')})
    )
    extra = 0
    max_num = 1

    exclude = ('password',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (TickleUserInline, PurchaseInline,)

    list_display = ('first_name', 'last_name', 'pid', 'email', 'phone', 'liu_id', 'notes')
    list_display_links = ('first_name', 'last_name', 'pid')
    list_filter = ('special_nutrition',)

    filter_horizontal = ('special_nutrition',)
    
    search_fields = ('first_name', 'last_name', 'email', 'liu_id', 'notes')

    actions = ['generate_email_recipient_list_action', 'fill_kobra_data_action']

    def fill_kobra_data_action(self, request, queryset):
        queryset.fill_kobra_data()
        self.message_user(request, _('Fetched KOBRA data.'))

    fill_kobra_data_action.short_description = _('Fetch KOBRA data (use with caution)')

    def generate_email_recipient_list_action(self, request, queryset):
        context = {
            'recipients': queryset.pretty_emails_string()
        }
        return TemplateResponse(request, 'tickle/admin/person/email_recipient_list.html', context)
    generate_email_recipient_list_action.short_description = _('Generate email recipient list')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_filter = ('content_type',)


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


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentUnionDiscount)
class StudentUnionDiscountAdmin(admin.ModelAdmin):
    pass
