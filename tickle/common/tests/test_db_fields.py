from __future__ import absolute_import, unicode_literals

from django.core.exceptions import ValidationError
from django.test import TestCase

from hamcrest import *

from ..db.fields import DescriptionField, MoneyField, NameField, NullCharField, SlugField


class DescriptionFieldTests(TestCase):
    def test_init(self):
        field = DescriptionField()
        assert_that(field.blank, equal_to(True))

        field = DescriptionField(blank=False)
        assert_that(field.blank, equal_to(False))


class MoneyFieldTests(TestCase):
    def test_init(self):
        field = MoneyField()
        assert_that(field.max_digits, equal_to(12))
        assert_that(field.decimal_places, equal_to(2))

        field = MoneyField(max_digits=9, decimal_places=3)
        assert_that(field.max_digits, equal_to(9))
        assert_that(field.decimal_places, equal_to(2))


class NameFieldTests(TestCase):
    def test_init(self):
        field = NameField()
        assert_that(field.max_length, equal_to(64))

        field = NameField(max_length=32)
        assert_that(field.max_length, equal_to(32))

    def test_clean(self):
        field = NameField()
        assert_that(
            calling(field.clean).with_args(value='', model_instance=None),
            raises(ValidationError))
        assert_that(
            calling(field.clean).with_args(value='   ', model_instance=None),
            raises(ValidationError))
        assert_that(field.clean(value='test', model_instance=None),
                    equal_to('test'))
        assert_that(field.clean(value=' test ', model_instance=None),
                    equal_to('test'))


class NullCharFieldTests(TestCase):
    def test_init(self):
        field = NullCharField()
        assert_that(field.null, equal_to(True))
        assert_that(field.blank, equal_to(True))
        assert_that(field.default, equal_to(None))

        field = NullCharField(null=False, blank=False, default='')
        assert_that(field.null, equal_to(True))
        assert_that(field.blank, equal_to(True))
        assert_that(field.default, equal_to(None))

    def test_clean(self):
        field = NullCharField(max_length=4)
        assert_that(field.clean(value='', model_instance=None),
                    equal_to(None))
        assert_that(field.clean(value=' ', model_instance=None),
                    equal_to(' '))
        assert_that(field.clean(value='test', model_instance=None),
                    equal_to('test'))


class SlugFieldTests(TestCase):
    def test_init(self):
        field = SlugField()
        assert_that(field.max_length, equal_to(64))

        field = SlugField(max_length=32)
        assert_that(field.max_length, equal_to(32))
