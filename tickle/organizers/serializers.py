from __future__ import absolute_import, unicode_literals

from tickle.common.serializers import HyperlinkedModelSerializer
from .models import Organizer


class OrganizerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organizer
        fields = [
            'url',
            'name',
            'slug'
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
