import logging
import json

from django.conf import settings
from django.db.models import Q
import django_filters
from rest_framework import filters

from .models import Ticket

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


class TicketOwnershipFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if view.action == 'search':
            search_term = request.query_params['query'].strip()
            query = (
                Q(pk__icontains=search_term) |
                Q(code__icontains=search_term) |
                Q(user__nin__contains=search_term.replace('-', '')) |
                Q(user__email__icontains=search_term)
            )

            if search_term.isdigit():
                try:
                    sesam_response = settings.SESAM_STUDENT_SERVICE_CLIENT.get_student(
                        mifare_id=search_term)
                except:
                    pass
                else:
                    query |= Q(user__email=sesam_response.email)

            if search_term.startswith('{'):
                try:
                    json_payload = json.loads(search_term)
                    query = Q(id=json_payload['id'], code=json_payload['code'])
                except:
                    pass

            return queryset.filter(query)

        if request.user.is_staff:
            return queryset

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
