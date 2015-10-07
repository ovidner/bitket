from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy

from tickle.common.factories import NameSlugFactoryMixin

from .models import Organizer, MainEvent


class OrganizerFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    class Meta:
        model = Organizer


class MainEventFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    organizer = factory.SubFactory(OrganizerFactory)

    class Meta:
        model = MainEvent
