# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


from tickle.models.products import Product, TicketType


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
    person = models.ForeignKey('tickle.Person', related_name='memberships')

    active = models.BooleanField(default=False, verbose_name=_('active member'))
    primary = models.BooleanField(default=False, verbose_name=_('primary orchestra'))

    approved = models.NullBooleanField()

    class Meta:
        unique_together = (('orchestra', 'person'),)

    def __str__(self):
        return u'{0}: {1}'.format(self.orchestra, self.person)


@python_2_unicode_compatible
class OrchestraMemberRegistration(models.Model):
    """
    Empty model used to mark Purchase objects as orchestra member registrations so we can fetch them in a deterministic
    way.
    """
    purchase = models.ForeignKey('tickle.Purchase', related_name='orchestra_member_registrations')

    def __str__(self):
        return self.purchase


@python_2_unicode_compatible
class OrchestraTicketType(models.Model):
    ticket_type = models.OneToOneField('tickle.TicketType', related_name='orchestra_ticket_type')

    # Which food object will you get when purchasing this ticket with food?
    food_ticket_type = models.ForeignKey('tickle.TicketType', related_name='+', null=True, blank=True)

    # Which food object will you get when purchasing this ticket with accommodation?
    accommodation_ticket_type = models.ForeignKey('tickle.TicketType', related_name='+', null=True, blank=True)

    dinner_ticket_type = models.ForeignKey('tickle.TicketType', related_name='+', null=True, blank=True)

    def __str__(self):
        return self.ticket_type.name

class OrchestraProductQuerySet(models.QuerySet):
    def stuff(self):
        return self.exclude(pk__in=TicketType.objects.all())

class OrchestraProduct(Product):
    objects = OrchestraProductQuerySet.as_manager()

    class Meta:
        proxy = True