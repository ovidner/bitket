# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


from tickle.models.products import Product


def get_anniversary_dinner_product():
    return Product.objects.get(pk=1)


@python_2_unicode_compatible
class Orchestra(models.Model):
    name = models.CharField(max_length=256)

    members = models.ManyToManyField('tickle.Person', related_name='orchestras', through='OrchestraMembership')

    class Meta:
        ordering = ['name']

        permissions = (
            ('approve_members', _('Approve members')),
        )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class OrchestraMembership(models.Model):
    orchestra = models.ForeignKey('Orchestra', related_name='memberships')
    member = models.ForeignKey('tickle.Person', related_name='memberships')

    active = models.BooleanField(default=False, verbose_name=_('active member'))
    primary = models.BooleanField(default=False, verbose_name=_('primary orchestra'))

    approved = models.NullBooleanField()

    class Meta:
        unique_together = (('orchestra', 'member'),)

    def __str__(self):
        return '{0}: {1}'.format(self.orchestra, self.member)


@python_2_unicode_compatible
class OrchestraMember(models.Model):
    person = models.OneToOneField('tickle.Person', related_name='orchestra_member')

    # Used to find and confirm the Purchase object in a predictable way
    # purchase_object = models.ForeignKey('tickle.Purchase')

    def __str__(self):
        return self.person.full_name


@python_2_unicode_compatible
class OrchestraTicketType(models.Model):
    ticket_type = models.OneToOneField('tickle.TicketType', related_name='orchestra_ticket_type')

    # Which food object will you get when purchasing this ticket with food?
    food_ticket_type = models.ForeignKey('tickle.TicketType', related_name='orchestra_ticket_type_food', null=True, blank=True)

    # Which food object will you get when purchasing this ticket with accommodation?
    accommodation_ticket_type = models.ForeignKey('tickle.TicketType', related_name='orchestra_ticket_type_accommodation', null=True, blank=True)

    def __str__(self):
        return self.ticket_type.product.name