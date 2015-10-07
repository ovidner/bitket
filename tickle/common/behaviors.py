from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class NameMixin(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class NameSlugMixin(NameMixin):
    class Meta:
        abstract = True


class NameSlugDescriptionMixin(NameSlugMixin):
    class Meta:
        abstract = True


class OrderedMixin(models.Model):
    order = models.PositiveIntegerField(
        verbose_name=_('order'))

    class Meta:
        abstract = True
