from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy
from autoslug.utils import slugify
from django.contrib.auth.hashers import make_password

from tickle.models import Condition, StudentUnionMemberCondition, Organizer, \
    MainEvent, ProductModifier, HoldingModifier, Person, StudentUnion, Cart, \
    Product, Holding

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
        model = Condition


class StudentUnionMemberConditionFactory(ConditionFactory):
    student_union = factory.SubFactory(StudentUnionFactory)

    class Meta:
        model = StudentUnionMemberCondition


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


class ProductModifierFactory(factory.DjangoModelFactory):
    condition = factory.SubFactory(ConditionFactory)
    product = factory.SubFactory(ProductFactory)

    delta_amount = factory.fuzzy.FuzzyInteger(-100, 40)

    order = factory.Sequence(lambda x: x)

    class Meta:
        model = ProductModifier


class HoldingModifierFactory(factory.DjangoModelFactory):
    product_modifier = factory.SubFactory(ProductModifierFactory)
    holding = factory.SubFactory(HoldingFactory)

    class Meta:
        model = HoldingModifier


class PersonFactory(factory.DjangoModelFactory):
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()

    email = factory.LazyAttribute(
        lambda o: '{}.{}@example.com'.format(o.first_name.strip(),
                                             o.last_name.strip()))

    password = factory.LazyAttribute(lambda o: make_password(None))

    class Meta:
        model = Person


class StudentUnionFactory(factory.DjangoModelFactory):
    name = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda o: slugify(o.name))

    class Meta:
        model = StudentUnion


class CartFactory(factory.DjangoModelFactory):
    person = factory.SubFactory(PersonFactory)

    class Meta:
        model = Cart


class ProductFactory(NameSlugDescriptionFactoryMixin):
    main_event = factory.SubFactory(MainEventFactory)
    base_price = factory.fuzzy.FuzzyDecimal(10, 1000)
    total_limit = factory.fuzzy.FuzzyInteger(750, 1000)

    class Meta:
        model = Product


class HoldingFactory(factory.DjangoModelFactory):
    cart = factory.SubFactory(CartFactory)
    person = factory.SubFactory(PersonFactory)
    product = factory.SubFactory(ProductFactory)

    class Meta:
        model = Holding
