from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy

from tickle.common.factories import NameSlugDescriptionFactoryMixin
from tickle.events.factories import MainEventFactory, OrganizerFactory
from tickle.people.factories import PersonFactory
from .models import Cart, Holding, Product


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
