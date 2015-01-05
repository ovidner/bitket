# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Orchestra(models.Model):
    name = models.CharField(max_length=256)

    members = models.ManyToManyField('OrchestraMember', related_name='orchestras', through='OrchestraMembership')

    class Meta:
        permissions = (
            ('approve_members', _('Approve members')),
        )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class OrchestraMembership(models.Model):
    orchestra = models.ForeignKey('Orchestra', related_name='memberships')
    member = models.ForeignKey('OrchestraMember', related_name='memberships')

    active = models.BooleanField(default=False)
    primary = models.BooleanField(default=False)

    approved = models.NullBooleanField()

    class Meta:
        unique_together = (('orchestra', 'member'),)

    def __str__(self):
        return '{0}: {1}'.format(self.orchestra, self.member)


@python_2_unicode_compatible
class OrchestraMember(models.Model):
    person = models.OneToOneField('tickle.Person', related_name='orchestra_member')

    def __str__(self):
        return self.person.full_name


@python_2_unicode_compatible
class OrchestraProduct(models.Model):
    product = models.OneToOneField('tickle.Product', related_name='orchestra_product')

    def __str__(self):
        return self.product.name