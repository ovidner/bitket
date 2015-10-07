from __future__ import absolute_import, unicode_literals

import factory, factory.fuzzy
from autoslug.utils import slugify

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
