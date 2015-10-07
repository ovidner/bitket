# -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.utils.timezone import now

from fungus.models import Shift, ShiftRegistration
from fungus.api.serializers import ShiftSerializer, ShiftRegistrationSerializer


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class ShiftRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ShiftRegistration.objects.all()
    serializer_class = ShiftRegistrationSerializer

    @detail_route(methods=['put', 'patch'], url_path='check-in')
    def check_in(self, request, pk=None):
        shift_registration = self.get_object()

        shift_registration.checked_in = now()
        shift_registration.save()

        return Response({'status': 'checked in'})

    @detail_route(methods=['put', 'patch', 'delete'], url_path='uncheck-in')
    def uncheck_in(self, request, pk=None):
        shift_registration = self.get_object()

        shift_registration.checked_in = None
        shift_registration.save()

        return Response({'status': 'unchecked in'})

    @detail_route(methods=['post'], url_path='check-out')
    def check_out(self, request, pk=None):
        shift_registration = self.get_object()

        shift_registration.checked_out = now()
        shift_registration.save()

        return Response({'status': 'checked out'})

    @detail_route(methods=['post', 'delete'], url_path='uncheck-out')
    def uncheck_out(self, request, pk=None):
        shift_registration = self.get_object()

        shift_registration.checked_in = None
        shift_registration.save()

        return Response({'status': 'unchecked in'})

