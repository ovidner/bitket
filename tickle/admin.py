# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.views.main import ChangeList
from django import forms
from django.db.models import Count
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from guardian.models import UserObjectPermission, GroupObjectPermission
from suit.admin import SortableTabularInline, SortableModelAdmin

from tickle.models import Person, Event, Product, Holding, TicketType, Delivery, Purchase, SpecialNutrition, \
    TickleUser, StudentUnionDiscount, ProductDiscount, Discount, HoldingDiscount, PersonalDiscount, DiscountEligibility
from tickle.views.admin import AddProductToShoppingCartAdminView


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
    list_display = ('person', 'product',)
    list_filter = ('product',)
    
    raw_id_fields = ('person', 'purchase', 'shopping_cart',)
    inlines = (HoldingDiscountInline,)

    search_fields = ('person__first_name', 'person__last_name', 'person__email', 'person__liu_id', 'person__pid_code')


@admin.register(TicketType)
class TicketTypeAdmin(ProductAdmin):
    filter_horizontal = ('events',)


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

    search_fields = ('person__first_name', 'person__last_name', 'person__email', 'person__liu_id', 'person__pid_code')


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


class DiscountEligibilityInline(admin.TabularInline):
    model = DiscountEligibility
    extra = 0
    can_delete = 0
    readonly_fields = ('discount',)

    def has_add_permission(self, request):
        return False


class EventVisitorListFilter(admin.SimpleListFilter):
    title = _('event')

    parameter_name = 'event'

    def lookups(self, request, model_admin):
        return [(i.pk, i.name) for i in Event.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            event = Event.objects.get(pk=self.value())
            return queryset.filter(holdings__product__ticket_type__events=event)
        else:
            return queryset


class PersonChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        super(PersonChangeList, self).get_results(*args, **kwargs)

        self.special_nutrition_totals = self.queryset.order_by().values(
            'special_nutrition__name').annotate(Count('pk'))


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (DiscountEligibilityInline, PurchaseInline, TickleUserInline,)

    list_display = ('first_name', 'last_name', 'pid', 'email', 'phone', 'liu_id', 'special_nutrition_render', 'notes')
    list_display_links = ('first_name', 'last_name', 'pid')
    list_filter = ('special_nutrition', EventVisitorListFilter)

    filter_horizontal = ('special_nutrition',)
    
    search_fields = ('first_name', 'last_name', 'email', 'liu_id', 'notes', 'pid_code')

    actions = ['generate_email_recipient_list_action',
               'fill_kobra_data_action',
               'create_user_action',
               'reset_password_action',
               'add_product_to_shopping_cart_action']

    list_max_show_all = 2000

    def get_urls(self):
        from django.conf.urls import url
        urls = super(PersonAdmin, self).get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        custom_urls = [
            url(r'^add-product/$', AddProductToShoppingCartAdminView.as_view(), name='%s_%s_add_product' % info),
        ]

        return custom_urls + urls  # Add our own first so the pk filter won't catch them

    def get_changelist(self, request, **kwargs):
        return PersonChangeList

    def special_nutrition_render(self, obj):
        items = obj.special_nutrition.values_list('name', flat=True)
        if not items:
            return ''

        output = '<ul>'
        for i in items:
            output += '<li>{0}</li>'.format(i)
        output += '</ul>'
        return output

    special_nutrition_render.short_description = _('special nutrition')
    special_nutrition_render.allow_tags = True
    special_nutrition_render.admin_order_field = 'special_nutrition'

    def create_user_action(self, request, queryset):
        for person in queryset:
            person.get_or_create_user()
        self.message_user(request, _('Created user accounts.'))

    create_user_action.short_description = _('Create user accounts (if not existing)')

    def reset_password_action(self, request, queryset):
        for person in queryset:
            if hasattr(person, 'user') and not getattr(person, 'liu_id'):
                person.user.generate_and_send_password()
        self.message_user(request, _('Reset and sent passwords.'))

    reset_password_action.short_description = _('Reset passwords')

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

    def add_product_to_shopping_cart_action(self, request, queryset):
        selected = queryset.values_list('pk', flat=True)
        # selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        return HttpResponseRedirect('add-product/?ids=%s' % ",".join(map(str, selected)))

    add_product_to_shopping_cart_action.short_description = _('Add product to shopping cart...')


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


@admin.register(PersonalDiscount)
class PersonalDiscountAdmin(admin.ModelAdmin):
    filter_horizontal = ('people',)
