# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tickle.models import Person

@python_2_unicode_compatible
class Orchestra(models.Model):
    name = models.CharField(max_length=256)
    bulk_invoicing = models.BooleanField(default=False)  # todo: should probably be done some other way

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class OrchestraMembership(models.Model):
    orchestra = models.ForeignKey('Orchestra')
    member = models.ForeignKey('OrchestraMember')
    # todo: add more fields declaring the relationship to the orchestra

    def __str__(self):
        return '{0}: {1}'.format(self.orchestra, self.person)

@python_2_unicode_compatible
class OrchestraMember(Person):
    orchestras = models.ManyToManyField('Orchestra', through='OrchestraMembership', null=True, blank=True)

    def __str__(self):
        return '{0} ({1})'.format(self.full_name, self.orchestra.name)