# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from tickle.models import Product, TicketType, Purchase, Person, Holding
from invar.models import generate_invoice


class OrchestraQuerySet(models.QuerySet):
    def invoice(self):
        for orch in self:
            members = orch.memberships.invoicable()
            # get the stuff each member has ordered
            total_stuff = []
            for member in members:
                stuff = Holding.objects.filter(person=member.person)
                for thing in stuff:
                    product = thing.product
                    # print(product)
                    quantity = thing.quantity
                    total_stuff.append((product, quantity, Person(member.person)))
                    #print(total_stuff)
            generate_invoice(orch.contact.full_name, orch.contact.email, orch.name, orch.organisation_number,
                             total_stuff)


@python_2_unicode_compatible
class Orchestra(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    organisation_number = models.CharField(max_length=11, blank=True, default='', verbose_name=_('organisation number'))

    members = models.ManyToManyField('tickle.Person', related_name='orchestras', through='OrchestraMembership',
                                     verbose_name=_('members'))

    contact = models.ForeignKey('tickle.Person', related_name='orchestra_contacts', null=True, blank=True, verbose_name='contact')

    objects = OrchestraQuerySet.as_manager()

    class Meta:
        ordering = ['name']

        permissions = (
            ('approve_orchestra_members', _('Approve orchestra members')),
        )

        verbose_name = _('orchestra')
        verbose_name_plural = _('orchestras')

    def __str__(self):
        return self.name


class OrchestraMembershipQuerySet(models.QuerySet):
    def get_primary(self):
        """
        Convenience method, preferably for returning a person's primary orchestra membership. Will raise an exception if
        multiple memberships are found. This is Django's standard behavior and we want to keep it – but keep it in mind.
        """
        return self.get(primary=True)

    def primary(self):
        return self.filter(primary=True)

    def approved(self):
        return self.filter(approved=True)

    def invoicable(self):
        return self.primary().approved()

    def people(self):
        return Person.objects.filter(orchestra_memberships__in=self)

    def purchases(self):
        return Purchase.objects.filter(person__in=self.people(), orchestra_member_registration__isnull=False)


@python_2_unicode_compatible
class OrchestraMembership(models.Model):
    orchestra = models.ForeignKey('Orchestra', related_name='memberships', verbose_name=_('orchestra'))
    person = models.ForeignKey('tickle.Person', related_name='orchestra_memberships', verbose_name=_('person'))

    primary = models.BooleanField(default=False, verbose_name=_('primary orchestra'))

    approved = models.NullBooleanField()

    objects = OrchestraMembershipQuerySet.as_manager()

    class Meta:
        unique_together = (('orchestra', 'person'),)

        verbose_name = _('orchestra membership')
        verbose_name_plural = _('orchestra memberships')

    def __str__(self):
        return u'{0}: {1}'.format(self.orchestra, self.person)


@python_2_unicode_compatible
class OrchestraMemberRegistration(models.Model):
    """
    Empty model used to mark Purchase objects as orchestra member registrations so we can fetch them in a deterministic
    way.
    """
    purchase = models.OneToOneField('tickle.Purchase', related_name='orchestra_member_registration',
                                    verbose_name=_('purchase'))

    class Meta:
        verbose_name = _('orchestra member registration')
        verbose_name_plural = _('orchestra member registrations')

    def __str__(self):
        return self.purchase.__str__()


@python_2_unicode_compatible
class OrchestraTicketType(models.Model):
    ticket_type = models.OneToOneField('tickle.TicketType', related_name='orchestra_ticket_type',
                                       verbose_name=_('ticket type'))

    # Which food object will you get when purchasing this ticket with food?
    food_ticket_type = models.ForeignKey('tickle.TicketType', related_name='+', null=True, blank=True,
                                         verbose_name=_('food ticket type'))

    # Which food object will you get when purchasing this ticket with accommodation?
    accommodation_ticket_type = models.ForeignKey('tickle.TicketType', related_name='+', null=True, blank=True,
                                                  verbose_name=_('accommodation ticket type'))

    jubilarian_10_ticket_type = models.ForeignKey('tickle.TicketType', related_name='+', null=True, blank=True,
                                                  verbose_name=_('10th festival ticket type'))
    jubilarian_25_ticket_type = models.ForeignKey('tickle.TicketType', related_name='+', null=True, blank=True,
                                                  verbose_name=_('25th festival ticket type'))

    class Meta:
        verbose_name = _('orchestra ticket type')
        verbose_name_plural = _('orchestra ticket types')

    def __str__(self):
        return self.ticket_type.name


class OrchestraProductQuerySet(models.QuerySet):
    def stuff(self):
        return self.exclude(pk__in=TicketType.objects.all())


class OrchestraProduct(Product):
    objects = OrchestraProductQuerySet.as_manager()

    class Meta:
        proxy = True

        verbose_name = _('product')
        verbose_name_plural = _('products')
