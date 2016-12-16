from __future__ import absolute_import, unicode_literals
import logging

from django.db.models import Q
import django_filters
from rest_framework import filters

from tickle.models import Ticket

logger = logging.getLogger(__name__)


class IsNullFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'{}__isnull'.format(self.name): value})
        return qs


class IsNotNullFilter(IsNullFilter):
    def filter(self, qs, value):
        if value is not None:
            value = not value
        return super(IsNotNullFilter, self).filter(qs, value)


class HoldingFilterSet(django_filters.FilterSet):
    liu_card = django_filters.CharFilter(name='person__liu_card_rfid')
    liu_id = django_filters.CharFilter(name='person__liu_id')
    purchased = IsNotNullFilter(name='cart__purchased')

    class Meta:
        model = Ticket
        fields = [
            'id',
            'liu_card',
            'liu_id',
            'purchased'
        ]


class TicketPermissionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_anonymous:
            return queryset.none()
        return queryset.owned_by(user=request.user, only_current=False)


class TicketOwnershipPermissionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_anonymous:
            return queryset.none()

        query = Q(user=request.user)

        code = request.query_params.get('code', None)
        if view.action != 'list' and code:
            query |= Q(code=code)
        return queryset.filter(query)


class UserPermissionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(pk=request.user.pk)
