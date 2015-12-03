from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy

from tickle.common.factories import NameSlugFactoryMixin
from django.conf import settings

from .models import MainEvent
from tickle.organizers.models import Organizer



class OrganizerFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    stripe_account_id = 'acct_15UmhTBnmRVIEGOy'
    stripe_refresh_token = 'rt_7BKd3RoiAGmUTFinVXmDG7UtY2uiWdHWEqCHzjfbRAe6PIsc'
    stripe_public_key = 'pk_test_ylCgAtl19NyJSCvrH7hR75F0'
    stripe_secret_key = 'sk_test_b6ayEDgcfTYU9j5GxTZYclfl'

    class Meta:
        model = Organizer


class MainEventFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    organizer = factory.SubFactory(OrganizerFactory)

    class Meta:
        model = MainEvent
