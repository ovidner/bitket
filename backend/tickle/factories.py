from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy
from autoslug.utils import slugify
from django.contrib.auth.hashers import make_password

from . import models

from .behaviors import NameSlugMixin, NameSlugDescriptionMixin


class NameSlugFactoryMixin(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda o: slugify(o.name))

    class Meta:
        model = NameSlugMixin
        abstract = True


class NameSlugDescriptionFactoryMixin(NameSlugFactoryMixin):
    description = factory.fuzzy.FuzzyText(length=64)

    class Meta:
        model = NameSlugDescriptionMixin
        abstract = True


class ConditionFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Condition





class OrganizationFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    stripe_account_id = 'acct_15UmhTBnmRVIEGOy'
    stripe_refresh_token = 'rt_7BKd3RoiAGmUTFinVXmDG7UtY2uiWdHWEqCHzjfbRAe6PIsc'
    stripe_public_key = 'pk_test_ylCgAtl19NyJSCvrH7hR75F0'
    stripe_secret_key = 'sk_test_b6ayEDgcfTYU9j5GxTZYclfl'

    class Meta:
        model = models.Organization


class EventFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    organization = factory.SubFactory(OrganizationFactory)

    class Meta:
        model = models.Event


class TicketTypeFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    description = factory.fuzzy.FuzzyText(length=64)
    event = factory.SubFactory(EventFactory)
    price = factory.fuzzy.FuzzyDecimal(10, 1000)
    max_total_quantity = factory.fuzzy.FuzzyInteger(750, 1000)

    class Meta:
        model = models.TicketType


class ModifierFactory(factory.DjangoModelFactory):
    condition = factory.SubFactory(ConditionFactory)
    ticket_type = factory.SubFactory(TicketTypeFactory)

    delta = factory.fuzzy.FuzzyInteger(-100, 40)

    class Meta:
        model = models.Modifier


class UserFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()

    email = factory.LazyAttribute(
        lambda o: '{}@example.com'.format(o.name))

    password = factory.LazyAttribute(lambda o: make_password(None))

    class Meta:
        model = models.User


class StudentUnionFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda o: slugify(o.name))

    class Meta:
        model = models.StudentUnion


class StudentUnionMemberConditionFactory(ConditionFactory):
    student_union = factory.SubFactory(StudentUnionFactory)

    class Meta:
        model = models.StudentUnionMemberCondition





class TicketFactory(factory.DjangoModelFactory):
    product = factory.SubFactory(TicketTypeFactory)

    class Meta:
        model = models.Ticket
