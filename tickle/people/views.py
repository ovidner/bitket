from __future__ import absolute_import, unicode_literals

from dry_rest_permissions.generics import DRYPermissionFiltersBase
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import list_route

from tickle.common.views import ModelViewSet
from .models import Person, StudentUnion
from .serializers import PersonSerializer, StudentUnionSerializer


class PersonFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        return queryset.filter(pk=request.user.pk)


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = (PersonFilterBackend,)

    @list_route()
    def current(self, request):
        qs = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(qs, pk=request.user.pk)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class StudentUnionViewSet(ModelViewSet):
    queryset = StudentUnion.objects.all()
    serializer_class = StudentUnionSerializer
    lookup_field = 'slug'
