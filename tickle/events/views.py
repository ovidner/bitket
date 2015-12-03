from __future__ import absolute_import, unicode_literals

from tickle.common.routers import parent_lookups
from tickle.common.views import ModelViewSet
from .models import MainEvent
from .serializers import MainEventSerializer


class MainEventViewSet(ModelViewSet):
    queryset = MainEvent.objects.all()
    serializer_class = MainEventSerializer
    lookup_field = 'slug'
    parent_lookups = parent_lookups.MAIN_EVENT
