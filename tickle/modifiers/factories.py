from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy

from tickle.conditions.factories import ConditionFactory
from tickle.products.factories import HoldingFactory, ProductFactory
from .models import ProductModifier, HoldingModifier


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
