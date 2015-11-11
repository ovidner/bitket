from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy

from tickle.common.factories import NameSlugFactoryMixin

from .models import MainEvent
from tickle.organizers.models import Organizer


class OrganizerFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    class Meta:
        model = Organizer


class MainEventFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    organizer = factory.SubFactory(OrganizerFactory)

    class Meta:
        model = MainEvent
