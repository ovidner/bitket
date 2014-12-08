# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Orchestra(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        permissions = (
            ('approve_members', _('Approve members')),
            ('approve_invoicing', _('Approve members for invoicing')),
        )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class OrchestraMembership(models.Model):
    orchestra = models.ForeignKey('Orchestra')
    member = models.ForeignKey('OrchestraMember')

    primary = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{0}: {1}'.format(self.orchestra, self.person)


@python_2_unicode_compatible
class OrchestraMember(models.Model):
    person = models.OneToOneField('tickle.Person', related_name='orchestra_member')

    orchestras = models.ManyToManyField('Orchestra', through='OrchestraMembership')

    def __str__(self):
        return '{0} ({1})'.format(self.person.full_name, self.orchestra.name)


@python_2_unicode_compatible
class OrchestraProduct(models.Model):
    product = models.OneToOneField('tickle.Product', related_name='orchestra_product')

    def __str__(self):
        return self.product.name