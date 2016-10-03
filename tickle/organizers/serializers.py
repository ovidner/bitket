from __future__ import absolute_import, unicode_literals

from ..common.serializers import HyperlinkedModelSerializer
from .models import Organizer


class OrganizerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organizer
        fields = [
            'url',
            'name',
            'slug',
            'main_events'
        ]
        expandable_fields = {
            'main_events': ('tickle.events.serializers.MainEventSerializer', (), {'many': True})
        }
