from __future__ import absolute_import, unicode_literals

from django.db.models import Q

import django_filters
from dry_rest_permissions.generics import DRYPermissionFiltersBase

from tickle.common.filters import IsNotNullFilter
from .models import Holding


class CartFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        return queryset.filter(person=request.user)


class HoldingPermissionFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        return queryset.filter(
            Q(person=request.user) |
            Q(cart__person=request.user) |
            Q(product__main_event__organizer__admins=request.user))


class HoldingFilterSet(django_filters.FilterSet):
    liu_card = django_filters.CharFilter(name='person__liu_card_rfid')
    liu_id = django_filters.CharFilter(name='person__liu_id')
    purchased = IsNotNullFilter(name='cart__purchased')

    class Meta:
        model = Holding
        fields = [
            'id',
            'liu_card',
            'liu_id',
            'purchased'
        ]
