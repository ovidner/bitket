from __future__ import absolute_import, unicode_literals

from django.contrib.auth.hashers import make_password

import factory, factory.fuzzy
from autoslug.utils import slugify

from .models import Person, StudentUnion


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
