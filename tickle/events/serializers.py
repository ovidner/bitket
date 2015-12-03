from __future__ import absolute_import, unicode_literals

from tickle.common.routers import parent_lookups
from tickle.common.serializers import HyperlinkedModelSerializer
from .models import MainEvent


class MainEventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MainEvent
        fields = [
            'url',
            'slug',
            'name',
            'description'
        ]
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug',
                'parent_lookups': parent_lookups.MAIN_EVENT
            }
        }

