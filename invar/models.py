# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from copy import deepcopy
from datetime import timedelta, date
from decimal import Decimal

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ungettext_lazy, ugettext_lazy as _
from django.utils.functional import cached_property
from django.db import models
from django.db.models import Sum, F, Q, ExpressionWrapper
from django.utils.timezone import now
from django.conf import settings

from tickle.utils.mail import TemplatedEmail
from invar.utils import ocr


def default_invoice_issue_date():
    return now()


def default_invoice_due_date():
    return now() + timedelta(days=settings.INVAR_DUE_DAYS)


class InvoiceQuerySet(models.QuerySet):
    def annotate_total(self):
        return self.annotate(
            annotated_total=ExpressionWrapper(
                Sum(F('rows__price') * F('rows__quantity')),
                # output_field MUST NOT have a max_digits specified!
                output_field=models.DecimalField(decimal_places=2)
            )
        )

    def annotate_payed(self):
        return self.annotate(
            annotated_payed=ExpressionWrapper(
                Sum('handle__transaction_matches__transaction__amount'),
                output_field=models.DecimalField(decimal_places=2)
            )
        )

    def payed(self):
        return self.annotate_total().annotate_payed().filter(
            Q(annotated_payed__exact=F('annotated_total')) |
            Q(annotated_payed__exact=None, annotated_total__exact=None) |
            Q(annotated_payed__exact=None, annotated_total__exact=0) |
            Q(annotated_payed__exact=0, annotated_total__exact=None)
        )

    def _unpayed(self):
        return self.annotate_total().annotate_payed().filter(
            Q(annotated_payed__lt=F('annotated_total')) |
            Q(annotated_payed__exact=None, annotated_total__gt=0)
        )

    def overdue(self):
        return self._unpayed().filter(due_date__lt=now().date())

    def pending(self):
        return self._unpayed().filter(due_date__gte=now().date())

    def overpayed(self):
        return self.annotate_total().annotate_payed().filter(
            Q(annotated_payed__gt=F('annotated_total')) |
            Q(annotated_payed__exact=None, annotated_total__lt=0)
        )

    def current(self):
        return self.filter(invalidation__isnull=True)

    def invalidated(self):
        return self.filter(invalidation__isnull=False,
                           invalidation__replacement__isnull=True)

    def replaced(self):
        return self.filter(invalidation__isnull=False,
                           invalidation__replacement__isnull=False)


@python_2_unicode_compatible
class Invoice(models.Model):
    receiver_name = models.CharField(max_length=255, blank=True, verbose_name=_('receiver name'))
    receiver_organisation = models.CharField(max_length=255, blank=True, verbose_name=_('receiver organisation'))
    receiver_pid = models.CharField(max_length=11, blank=True, verbose_name=_('receiver PID'))
    receiver_email = models.EmailField(verbose_name=_('receiver email address'))

    issue_date = models.DateField(null=True, blank=True, default=default_invoice_issue_date, verbose_name=_('issue date'))
    due_date = models.DateField(null=True, blank=True, default=default_invoice_due_date, verbose_name=_('due date'))

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        ordering = ('pk',)

        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    def __str__(self):
        return str(self.pk)

    def connect_handle(self):
        if not hasattr(self, 'invalidation') and not hasattr(self, 'handle'):
            InvoiceHandle.objects.create(invoice=self)

    @cached_property
    def ocr(self):
        return self.handle.ocr

    @cached_property
    def total(self):
        return self.rows.aggregate(total=ExpressionWrapper(Sum(F('price') * F('quantity')), output_field=models.DecimalField(decimal_places=2)))['total']

    @cached_property
    def payed(self):
        return self.handle.transaction_matches.all().aggregate(total=Sum('transaction__amount'))['total'] or Decimal('0.00')

    @cached_property
    def status(self):
        invalidation = getattr(self, 'invalidation', None)

        if invalidation:
            if getattr(invalidation, 'replacement', None):
                return 'replaced'
            else:
                return 'invalidated'
        else:
            return 'current'

    @cached_property
    def payment_status(self):
        if self.payed == self.total:
            return 'payed'
        elif self.payed > self.total:
            return 'overpayed'
        elif self.payed < self.total:
            if now().date() <= self.due_date:
                return 'pending'
            else:
                return 'overdue'

    def send(self, email=None):
        if self.total != 0:
            context = {
                'invoice': self,
                'bg': settings.INVAR_BG,
                'iban': settings.INVAR_IBAN,
                'bic_swift': settings.INVAR_BIC_SWIFT,
            }

            if not email:
                email = self.receiver_email

            mail = TemplatedEmail(subject_template='invar/email/invoice_subject.txt',
                                  body_template_html='invar/email/invoice.html', context=context,
                                  from_email="Faktura SOF15 <faktura@sof15.se>", to=[email],
                                  tags=['invar', 'invoice'])

            mail.send()

    def send_update(self):
        context = {
            'invoice': self,
            'bg': settings.INVAR_BG,
            'iban': settings.INVAR_IBAN,
            'bic_swift': settings.INVAR_BIC_SWIFT,
        }

        mail = TemplatedEmail(subject_template='invar/email/invoice_update_subject.txt',
                              body_template_html='invar/email/invoice_update.html', context=context,
                              from_email="Faktura SOF15 <faktura@sof15.se>", to=[self.receiver_email],
                              tags=['invar', 'invoice', 'update'])

        mail.send()

    def send_invalidation(self):
        context = {
            'invoice': self
        }

        mail = TemplatedEmail(subject_template='invar/email/invoice_invalidation_subject.txt',
                              body_template_html='invar/email/invoice_invalidation.html', context=context,
                              from_email="Faktura SOF15 <faktura@sof15.se>", to=[self.receiver_email],
                              tags=['invar', 'invoice', 'invalidation'])

        mail.send()

    def _copy_rows(self, target):
        for i in self.rows.all():
            i._copy_to(target)

    def copy(self, keep_dates=False):
        rows = self.rows.all()
        new = deepcopy(self)
        new.pk = None

        if not keep_dates:
            new.issue_date = now()
            new.due_date = now() + timedelta(days=settings.INVAR_DUE_DAYS)

        new.save()

        for i in rows:
            i._copy_to(new)

        return new

    def invalidate(self, replacement=None):
        invalidation = InvoiceInvalidation(invoice=self)

        if replacement:
            invalidation.replacement = replacement
            self.handle.invoice = replacement
            self.handle.save()

        invalidation.save()

        return invalidation


class InvoiceInvalidation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('timestamp'))
    invoice = models.OneToOneField('Invoice', related_name='invalidation', verbose_name=_('invoice'))
    replacement = models.OneToOneField('Invoice', related_name='replacing_invalidation', null=True, verbose_name=_('replacement invoice'))

    class Meta:
        verbose_name = _('invoice invalidation')
        verbose_name_plural = _('invoice invalidations')


class InvoiceHandleQuerySet(models.QuerySet):
    def get_ocr(self, n):
        if not ocr.verify(n):
            raise InvoiceHandle.DoesNotExist('Not a valid OCR number.')

        pk = int(ocr.strip(n))

        return self.get(pk=pk)


class InvoiceHandle(models.Model):
    invoice = models.OneToOneField('Invoice', related_name='handle', verbose_name=_('invoice'))

    objects = InvoiceHandleQuerySet.as_manager()

    class Meta:
        verbose_name = _('invoice handle')
        verbose_name_plural = _('invoice handles')

    def __str__(self):
        return self.ocr

    @property
    def ocr(self):
        return ocr.generate(self.id)


class PersonInvoiceHandle(models.Model):
    handle = models.OneToOneField('InvoiceHandle', related_name='person_handle', verbose_name=_('handle'))
    person = models.ForeignKey('tickle.Person', related_name='invoice_handles', verbose_name=_('person'))

    class Meta:
        verbose_name = _('personal invoice handle')
        verbose_name_plural = _('personal invoice handles')


class InvoiceRowQuerySet(models.QuerySet):
    pass


class InvoiceRow(models.Model):
    invoice = models.ForeignKey('Invoice', related_name='rows', verbose_name=_('invoice'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    person = models.CharField(max_length=256, blank=True, verbose_name=_('person'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('price'))

    objects = InvoiceRowQuerySet.as_manager()

    class Meta:
        verbose_name = _('invoice row')
        verbose_name_plural = _('invoice rows')

    def __str__(self):
        return str(self.pk)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def _copy_to(self, invoice):
        holding_row = self.holding_row
        self.pk = None
        self.invoice = invoice
        self.save()

        holding_row.pk = None
        holding_row.invoice_row = self
        holding_row.save()

    def _set_person(self, person):
        self.person = '{0} ({1})'.format(person.full_name, person.pid)


class HoldingInvoiceRowQuerySet(models.QuerySet):
    def current(self):
        return self.get(invoice_row__invoice__invalidation__isnull=True)

    def current_invoice(self):
        return self.current().invoice_row.invoice

    def invoice_rows(self):
        return InvoiceRow.objects.filter(holding_row__in=self)


class HoldingInvoiceRow(models.Model):
    invoice_row = models.OneToOneField('InvoiceRow', related_name='holding_row', verbose_name=_('invoice row'))
    holding = models.ForeignKey('tickle.Holding', related_name='holding_invoice_rows', verbose_name=_('holding'))

    objects = HoldingInvoiceRowQuerySet.as_manager()

    class Meta:
        verbose_name = _('holding invoice row')
        verbose_name_plural = _('holding invoice rows')


class TransactionQuerySet(models.QuerySet):
    def match_ocr(self):
        for i in self:
            i.match_ocr()

        return self


class Transaction(models.Model):
    timestamp = models.DateTimeField(default=now, verbose_name=_('timestamp'))
    amount = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('amount'))
    reference = models.CharField(max_length=256, verbose_name=_('reference'))
    uid = models.CharField(max_length=256, unique=True, null=True, blank=True, verbose_name=_('unique identifier'))

    objects = TransactionQuerySet.as_manager()

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')

    def match_ocr(self, fail_silently=True):
        try:
            handle = InvoiceHandle.objects.get_ocr(self.reference)
        except InvoiceHandle.DoesNotExist as e:
            if fail_silently:
                return None
            raise e

        match, created = TransactionMatch.objects.get_or_create(transaction=self, defaults={'handle': handle})

        if not created:
            match.handle = handle
            match.save()

        return match


class TransactionMatch(models.Model):
    transaction = models.OneToOneField('Transaction', related_name='match', verbose_name=_('transaction'))
    handle = models.ForeignKey('InvoiceHandle', related_name='transaction_matches', verbose_name=_('invoice handle'))

    class Meta:
        verbose_name = _('transaction match')
        verbose_name_plural = _('transaction matches')


class BgMaxImport(models.Model):
    file_name = models.CharField(max_length=256, verbose_name=_('file name'))
    file_sha1 = models.CharField(max_length=40, unique=True, verbose_name=_('file SHA1'))
    import_timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('import timestamp'))
    creation_timestamp = models.DateTimeField(verbose_name=_('creation timestamp'))

    # transactions = models.ManyToManyField('Transaction', related_name='bgmax_imports', verbose_name=_('transactions'))

    class Meta:
        verbose_name = _('BgMax import')
        verbose_name_plural = _('BgMax imports')

    def __str__(self):
        return '{0}'.format(self.import_timestamp)
