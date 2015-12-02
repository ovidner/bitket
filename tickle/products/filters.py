from __future__ import absolute_import, unicode_literals

from django.db.models import Q

from dry_rest_permissions.generics import DRYPermissionFiltersBase


class CartFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        return queryset.filter(person=request.user)


class HoldingFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        return queryset.filter(
            Q(person=request.user) | Q(cart__person=request.user))
