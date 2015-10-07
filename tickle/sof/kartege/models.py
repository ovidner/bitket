# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.db.transaction import atomic

from tickle.models import Person, PersonQuerySet, BaseDiscount


@python_2_unicode_compatible
class Material(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name=_('name'))
    unit = models.CharField(max_length=16, verbose_name=_('unit'))

    class Meta:
        verbose_name = _('material')
        verbose_name_plural = _('materials')

        ordering = ('-name',)

    def __str__(self):
        return '%s [%s]' % (self.name, self.unit)

    def total_amount(self):
        return self.entrymaterial_set.aggregate(amount=models.Sum('amount'))['amount']


@python_2_unicode_compatible
class MaterialRole(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    class Meta:
        verbose_name = _('material role')
        verbose_name_plural = _('material roles')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class EntryMaterial(models.Model):
    entry = models.ForeignKey('Entry', verbose_name=_('entry'))
    material = models.ForeignKey('Material', verbose_name=_('material'))

    amount = models.DecimalField(max_digits=9, decimal_places=3, verbose_name=_('amount'))
    role = models.ForeignKey('MaterialRole', verbose_name=_('role'))

    class Meta:
        ordering = ('entry', 'material', 'role')

        verbose_name = _('entry material')
        verbose_name_plural = _('entry materials')

    def __str__(self):
        return '%s: %s %s %s (%s)' % (
        self.entry.name, self.amount, self.material.unit, self.material.name, self.role.name)


@python_2_unicode_compatible
class EntryCustomMaterial(models.Model):
    entry = models.ForeignKey('Entry', verbose_name=_('entry'))
    material = models.CharField(max_length=512, verbose_name=_('material'))

    amount = models.DecimalField(max_digits=9, decimal_places=3, verbose_name=_('amount'))
    unit = models.CharField(max_length=8, verbose_name=_('unit'))
    role = models.ForeignKey('MaterialRole', verbose_name=_('role'))

    class Meta:
        verbose_name = _('entry custom material')
        verbose_name_plural = _('entry custom materials')

    def __str__(self):
        return '%s: %s %s %s (%s)' % (self.entry.name, self.amount, self.unit, self.material, self.role.name)


@python_2_unicode_compatible
class EntryType(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    description = models.CharField(max_length=256, verbose_name=_('description'))
    max_members = models.PositiveIntegerField(verbose_name=_('max members'))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('price'))

    class Meta:
        ordering = ('max_members', 'name',)

        verbose_name = _('entry type')
        verbose_name_plural = _('entry types')

    def __str__(self):
        return '%s (%s)' % (self.name, self.description)


class EntryQuerySet(models.QuerySet):
    def invoice(self, send=True):
        for i in self:
            i.invoice(send=send)

        return self

@python_2_unicode_compatible
class Entry(models.Model):
    constellation = models.CharField(max_length=256, verbose_name=_('constellation'),
                                     help_text=_('E.g. <em>MPiRE</em>, <em>Grabbarna Grus</em>'))
    name = models.CharField(max_length=256, verbose_name=_('entry name'))
    entry_type = models.ForeignKey('EntryType', related_name='entries', verbose_name=_('entry type'))
    members = models.PositiveIntegerField(default=10, verbose_name=_('number of members'))

    approved = models.BooleanField(default=False, verbose_name=_('approved'))

    # Fult som stryk!
    primary_contact_name = models.CharField(max_length=256, verbose_name=_('name'))
    primary_contact_address = models.CharField(max_length=256, verbose_name=_('address'))
    primary_contact_postcode = models.CharField(max_length=6, verbose_name=_('postcode'))
    primary_contact_city = models.CharField(max_length=64, verbose_name=_('city'))
    primary_contact_phone = models.CharField(max_length=256, verbose_name=_('phone'))
    primary_contact_email = models.EmailField(verbose_name=_('email'))

    secondary_contact_name = models.CharField(max_length=256, verbose_name=_('name'))
    secondary_contact_address = models.CharField(max_length=256, verbose_name=_('address'))
    secondary_contact_postcode = models.CharField(max_length=6, verbose_name=_('postcode'))
    secondary_contact_city = models.CharField(max_length=64, verbose_name=_('city'))
    secondary_contact_phone = models.CharField(max_length=256, verbose_name=_('phone'))
    secondary_contact_email = models.EmailField(verbose_name=_('email'))

    width = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_('width'),
                                help_text=_('Width in meters, in direction of movement.'))
    length = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_('length'),
                                 help_text=_('Length in meters, in direction of movement.'))
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_('height'),
                                 help_text=_('Height in meters.'))

    description = models.TextField(verbose_name=_('description'), help_text=_('Describe your idea! Maximum 500 words.'))
    spex_description = models.TextField(verbose_name=_('spex description'), help_text=_(
        'Describe what will happen in, on and around your carriage! Music, theatre or anything else amusing? Maximum '
        '500 words.'))
    other_information = models.TextField(blank=True, null=True, verbose_name=_('other information'),
                                         help_text=_('Want us to know something else?'))

    materials = models.ManyToManyField('Material', through='EntryMaterial')

    submitted = models.DateTimeField(auto_now_add=True)

    objects = EntryQuerySet.as_manager()

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

        ordering = ('constellation',)
        unique_together = (('constellation', 'name'),)

    def __str__(self):
        return self.constellation

    def invoice(self, send=True):
        from invar.models import Invoice, InvoiceRow

        invoice = Invoice(
            receiver_name=self.primary_contact_name,
            receiver_organisation=self.constellation,
            receiver_pid='',
            receiver_email=self.primary_contact_email,
        )

        invoice_row = InvoiceRow(
            title=self.entry_type.name,
            person=self.constellation,
            price=self.entry_type.price,
        )

        if not send:
            invoice.issue_date = None
            invoice.due_date = None

        with atomic():
            invoice.save()
            invoice.connect_handle()

            invoice_row.invoice = invoice
            invoice_row.save()

            EntryInvoiceHandle.objects.create(handle=invoice.handle, entry=self)

        # Problems with sending shouldn't break the transaction
        if send:
            invoice.send()

        return invoice


@python_2_unicode_compatible
class EntryMembership(models.Model):
    person = models.ForeignKey('tickle.Person', related_name='kartege_memberships', verbose_name=_('person'))
    entry = models.ForeignKey('Entry', related_name='memberships', verbose_name=_('entry'))

    class Meta:
        unique_together = (('person', 'entry'),)

        verbose_name = _('entry membership')
        verbose_name_plural = _('entry memberships')

    def __str__(self):
        return '{0}: {1}'.format(self.person, self.entry)


class KartegeMemberQuerySet(PersonQuerySet):
    def kartege_members(self):
        return self.filter(kartege_memberships__isnull=False)


class KartegeMember(Person):
    objects = KartegeMemberQuerySet.as_manager()

    class Meta:
        proxy = True

        verbose_name = _('Kårtege member')
        verbose_name_plural = _('Kårtege members')


@python_2_unicode_compatible
class KartegeMemberDiscount(BaseDiscount):
    class Meta:
        verbose_name = _('Kårtege member discount')
        verbose_name_plural = _('Kårtege member discounts')

    def __str__(self):
        return self.readable_discount()

    def eligible(self, person):
        return EntryMembership.objects.filter(person=person, entry__approved=True).exists()


class EntryInvoiceHandle(models.Model):
    handle = models.OneToOneField('invar.InvoiceHandle', related_name='kartege_entry_handle', verbose_name=_('handle'))
    entry = models.ForeignKey('Entry', related_name='invoice_handles', verbose_name=_('entry'))

    class Meta:
        verbose_name = _('Kårtege entry invoice handle')
        verbose_name_plural = _('Kårtege entry invoice handles')
