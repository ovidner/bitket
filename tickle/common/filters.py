from __future__ import absolute_import, unicode_literals
import logging
logger = logging.getLogger(__name__)

import django_filters


class IsNullFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'{}__isnull'.format(self.name): value})
        return qs


class IsNotNullFilter(IsNullFilter):
    def filter(self, qs, value):
        if value is not None:
            value = not value
        return super(IsNotNullFilter, self).filter(qs, value)
