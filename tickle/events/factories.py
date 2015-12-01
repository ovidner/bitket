from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy

from tickle.common.factories import NameSlugFactoryMixin
from django.conf import settings

from .models import MainEvent
from tickle.organizers.models import Organizer



class OrganizerFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    stripe_account_id = "acct_16oBUPJyXU6ClYwv"
    stripe_refresh_token = "rt_7SBELttVfPJZutvQGpMPXQfytec6rFEHNLT9cWTG0aV2nhsn"
    stripe_public_key = 'sk_test_mxObDuXVzXMZywWT1FiCcmBe'
    stripe_secret_key = 'pk_test_YssxGJY7xNnFSwuWB0kH355m'


    class Meta:
        model = Organizer


class MainEventFactory(NameSlugFactoryMixin, factory.DjangoModelFactory):
    organizer = factory.SubFactory(OrganizerFactory)

    class Meta:
        model = MainEvent
