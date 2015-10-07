from __future__ import absolute_import, unicode_literals

from decimal import Decimal

from django.test import TestCase
from django.core.exceptions import ValidationError

from hamcrest import *

from ..factories import ProductModifierFactory, HoldingModifierFactory
from tickle.products.factories import HoldingFactory, ProductFactory


class ProductModifierMethodTests(TestCase):
    def test_save(self):
        modifier = ProductModifierFactory.build()

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(calling(modifier.save), raises(ValidationError))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(calling(modifier.save), raises(ValidationError))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(calling(modifier.save), not_(raises(ValidationError)))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(calling(modifier.save), not_(raises(ValidationError)))

    def test_delta(self):
        modifier = ProductModifierFactory.build()

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(modifier.delta(), equal_to((None, None)))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.delta(), equal_to((None, None)))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(modifier.delta(), equal_to((Decimal('-100.00'), False)))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.delta(), equal_to((Decimal('-0.5'), True)))

    def test_real_delta(self):
        modifier = ProductModifierFactory.build(
            product__base_price=Decimal('1000.00'))

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(modifier.real_delta(), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(modifier.real_delta(), equal_to(Decimal('-100.00')))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(), equal_to(Decimal('-500.00')))

        modifier.delta_amount = None
        modifier.delta_factor = None
        assert_that(modifier.real_delta(Decimal('200.00')), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(Decimal('200.00')), equal_to(None))

        modifier.delta_amount = Decimal('-100.00')
        modifier.delta_factor = None
        assert_that(modifier.real_delta(Decimal('200.00')),
                    equal_to(Decimal('-100.00')))

        modifier.delta_amount = None
        modifier.delta_factor = Decimal('-0.5')
        assert_that(modifier.real_delta(Decimal('200.00')),
                    equal_to(Decimal('-100.00')))


class HoldingModifierMethodTests(TestCase):
    def test_save(self):
        product_1 = ProductFactory()
        product_2 = ProductFactory()

        product_modifier = ProductModifierFactory(product=product_1)
        holding = HoldingFactory(product=product_1)
        holding_modifier = HoldingModifierFactory.build(
            product_modifier=product_modifier,
            holding=holding)
