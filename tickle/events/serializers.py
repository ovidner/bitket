from __future__ import absolute_import, unicode_literals

from ..common.serializers import HyperlinkedModelSerializer
from .models import MainEvent


class MainEventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MainEvent
        fields = [
            'url',
            'id',
            'slug',
            'organizer',
            'name',
            'description'
        ]
        expandable_fields = {
            'organizer': ('tickle.organizers.serializers.OrganizerSerializer', (), {})
        }
