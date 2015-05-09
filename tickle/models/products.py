# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import Sum, Q
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db.transaction import atomic

from decimal import Decimal

from tickle.models.people import Person
from tickle.utils.mail import TemplatedEmail
from invar.models import InvoiceRow, HoldingInvoiceRow


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class EventQuerySet(models.QuerySet):
    def holdings(self):
        return Holding.objects.filter(product__ticket_type__events__in=self)

    def visitors(self):
        return self.holdings().purchased().holders()


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ('name',)
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)

    def ticket_types(self):
        return self.filter(ticket_type__isnull=False)

    def gadget_types(self):
        return self.filter(ticket_type__isnull=True)

    def holdings(self):
        return Holding.objects.filter(product__in=self)


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField(max_length=256, verbose_name=_('name'))
    _public_name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_('public name'))
    description = models.TextField(blank=True, verbose_name=_('description'))

    categories = models.ManyToManyField('Category', blank=True, verbose_name=_('categories'))

    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('price'))
    quantitative = models.BooleanField(default=False,
                                       verbose_name=_('quantitative'),
                                       help_text=_('Can you purchase more than one (1) of this product?'))

    published = models.BooleanField(default=True, verbose_name=_('published'))
    quota = models.PositiveIntegerField(default=0, verbose_name=_('quota'), blank=True,
                                        help_text=_('0 means there is no quota limit.'))
    transferable = models.BooleanField(default=True, verbose_name=_('transferable'),
                                       help_text=_('If people should be able to transfer this product to other people.'))

    order = models.PositiveIntegerField(verbose_name=_('order'))

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ('order',)

        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return self.name

    @property
    def public_name(self):
        return self._public_name or self.name

    @property
    def is_ticket_type(self):
        return bool(getattr(self, 'ticket_type', False))

    def has_reached_quota(self):
        return self.quota != 0 and self.holdings.purchased().quantity() >= self.quota


@python_2_unicode_compatible
class TicketType(Product):
    product = models.OneToOneField('Product', related_name='ticket_type', parent_link=True, verbose_name=_('product'))
    events = models.ManyToManyField('Event', related_name='ticket_types', blank=True, verbose_name=_('events'))

    class Meta:
        verbose_name = _('ticket type')
        verbose_name_plural = _('ticket types')

    def __str__(self):
        return self.product.name


class HoldingQuerySet(models.QuerySet):
    # METHODS RETURNING HOLDING QUERYSETS #

    def valid(self):
        return self.filter(invalidated=False)

    def invalid(self):
        return self.filter(invalidated=True)

    def purchased(self):
        return self.filter(purchase__isnull=False)

    def unpurchased(self):
        return self.filter(purchase__isnull=True)

    def invoiced(self):
        return self.filter(
            holding_invoice_rows__isnull=False,
            holding_invoice_rows__invoice_row__invoice__invalidation__isnull=True).distinct()

    def uninvoiced(self):
        return self.filter(
            Q(holding_invoice_rows__isnull=True) |
            ~Q(holding_invoice_rows__invoice_row__invoice__invalidation__isnull=True)).distinct()

    def tickets(self):
        return self.filter(product__ticket_type__isnull=False)

    def gadgets(self):
        return self.filter(product__ticket_type__isnull=True)

    # METHODS RETURNING OTHER QUERYSETS #

    def holders(self):
        return Person.objects.filter(holdings__in=self).distinct()

    # METHODS RETURNING NUMERIC VALUES #

    def total_cost(self):
        return self.annotate(price=Sum('product__price')).aggregate(Sum('price', field='price*quantity'))['price__sum']\
            or 0

    def discounted_total(self):
        total = Decimal("0.00")
        for i in self:
            total += i.discounted_total
        return total

    def quantity(self):
        return self.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # METHODS MANIPULATING DATA #

    def remap_discounts(self):
        with atomic():
            for i in self:
                print i
                i.remap_discounts()

    def add_to_invoice(self, invoice):
        for i in self:
            HoldingInvoiceRow.objects.create(
                holding=i,
                invoice_row=InvoiceRow.objects.create(
                    invoice=invoice,
                    title=i.product.public_name,
                    person='{0} ({1})'.format(i.person.full_name, i.person.pid),
                    quantity=i.quantity,
                    price=i.discounted_price),
            )

    def invoice_person(self, person, send=True):
        if not self:
            return

        from invar.models import Invoice, PersonInvoiceHandle

        invoice = Invoice(
            receiver_name=person.full_name,
            receiver_organisation='',
            receiver_pid=person.pid or '',
            receiver_email=person.email,
        )

        if not send:
            invoice.issue_date = None
            invoice.due_date = None

        with atomic():
            invoice.save()
            invoice.connect_handle()
            PersonInvoiceHandle.objects.create(handle=invoice.handle, person=person)
            self.add_to_invoice(invoice)

        # Problems with sending shouldn't break the transaction
        if send:
            invoice.send()

        return invoice


@python_2_unicode_compatible
class Holding(models.Model):
    person = models.ForeignKey('Person', related_name='holdings', verbose_name=_('person'))
    product = models.ForeignKey('Product', related_name='holdings', verbose_name=_('product'))

    purchase = models.ForeignKey('Purchase', related_name='holdings', null=True, blank=True, verbose_name=_('purchase'))
    shopping_cart = models.ForeignKey('ShoppingCart', related_name='holdings', null=True, blank=True,
                                      verbose_name=_('shopping cart'))

    _transferable = models.NullBooleanField(default=None, verbose_name=_('transferable'),
                                            help_text=_('If people should be able to transfer this product to other people. Note: this will override the product setting.'))

    quantity = models.PositiveIntegerField(default=1, verbose_name=_('quantity'))

    invalidated = models.BooleanField(default=False, verbose_name=_('invalidated'))

    objects = HoldingQuerySet.as_manager()

    class Meta:
        verbose_name = _('holding')
        verbose_name_plural = _('holdings')

    def __str__(self):
        return u'{0} {1}'.format(self.product, self.person)

    def clean(self):
        if not self.product.quantitative and not self.quantity == 1:
            raise ValidationError(_('Quantity must be exactly 1 for un-quantitative products.'))

    def save(self, *args, **kwargs):
        shopping_cart = getattr(self, 'shopping_cart')
        purchase = getattr(self, 'purchase')
        if shopping_cart and purchase:
            raise ValidationError(_("Can't hold both a shopping cart and a purchase at the same time."))
        elif not shopping_cart and not purchase:
            raise ValidationError(_('Holding must have either a shopping cart or a purchase.'))

        return super(Holding, self).save(*args, **kwargs)

    def send_ticket(self):
        msg = TemplatedEmail(
            to=[self.person.pretty_email],
            from_email='Biljett SOF15 <biljett@sof15.se>',
            subject_template='tickle/email/ticket_subject.txt',
            body_template_html='tickle/email/ticket.html',
            context={
                'holding': self,
            },
            tags=['tickle', 'ticket'])
        msg.send()

    @cached_property
    def discounted_price(self):
        price = self.product.price
        if getattr(self, 'purchase'):
            # Calculate by HoldingDiscounts if purchased
            for i in self.holding_discounts.all():
                price -= i.discount.delta(price)
        else:
            # Else calculate by ProductDiscounts
            for i in self.product.product_discounts.eligible(self.person):
                price -= i.discount.delta(price)

        return price

    def remap_discounts(self):
        if self.purchase:
            self.holding_discounts.all().delete()
            self.product.product_discounts.eligible(person=self.person).copy_to_holding_discounts(holding=self)

    @cached_property
    def discounted_total(self):
        return self.discounted_price * self.quantity

    def _get_transferable(self):
        if self._transferable is None:
            return self.product.transferable
        return self._transferable

    def _set_transferable(self, value):
        self._transferable = value

    transferable = property(_get_transferable, _set_transferable)

    @property
    def total(self):
        return self.product.price * self.quantity


@python_2_unicode_compatible
class Delivery(models.Model):
    holdings = models.ManyToManyField('Holding', verbose_name=_('holdings'))
    delivered = models.DateTimeField(verbose_name=_('delivered'))

    class Meta:
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')

    def __str__(self):
        return u'{0}, {1}'.format(self.holdings, self.delivered)


@python_2_unicode_compatible
class ShoppingCart(models.Model):
    person = models.OneToOneField('Person', related_name='shopping_cart', verbose_name=_('person'))

    class Meta:
        verbose_name = _('shopping cart')
        verbose_name_plural = _('shopping carts')

    def __str__(self):
        return self.person.full_name

    def purchase(self):
        with atomic():
            holdings = self.holdings.all()

            for holding in holdings:
                if holding.product.has_reached_quota():
                    raise Exception(holding.product)

            purchase = Purchase.objects.create(person=self.person, purchased=now())

            for holding in holdings:
                holding.shopping_cart = None
                holding.purchase = purchase

                # This copies all eligible discounts to the holding object
                holding.product.product_discounts.eligible(self.person).copy_to_holding_discounts(holding)

                holding.save()

            holdings.invoice_person(self.person)


class PurchaseQuerySet(models.QuerySet):
    def holdings(self):
        return Holding.objects.filter(purchase__in=self)


@python_2_unicode_compatible
class Purchase(models.Model):
    person = models.ForeignKey('Person', verbose_name=_('person'))
    purchased = models.DateTimeField(verbose_name=_('purchased'))

    valid = models.BooleanField(default=True, verbose_name=_('valid'))

    objects = PurchaseQuerySet.as_manager()

    class Meta:
        verbose_name = _('purchase')
        verbose_name_plural = _('purchases')

    def __str__(self):
        return u'{0} – {1}'.format(self.person, self.purchased)
