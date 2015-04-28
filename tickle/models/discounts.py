# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from decimal import Decimal

from tickle.utils.format import format_percent


@python_2_unicode_compatible
class DiscountEligibility(models.Model):
    """
    Denormalized model storing eligibilities for discounts.
    """

    discount = models.ForeignKey('Discount', related_name='eligibilities')
    person = models.ForeignKey('Person', related_name='discount_eligibilities')

    class Meta:
        unique_together = (('discount', 'person'),)

        verbose_name = _('discount eligibility')
        verbose_name_plural = _('discount eligibilities')

    def __str__(self):
        return '{0} – {1}'.format(self.person, self.discount)


@python_2_unicode_compatible
class HoldingDiscount(models.Model):
    holding = models.ForeignKey('Holding', related_name='holding_discounts', verbose_name=_('holding'))
    discount = models.ForeignKey('Discount', related_name='holding_discounts', verbose_name=_('discount'))

    order = models.PositiveIntegerField(verbose_name=_('order'))

    class Meta:
        ordering = ('order',)
        unique_together = (('holding', 'discount'),)

        verbose_name = _('holding discount')
        verbose_name_plural = _('holding discounts')

    def __str__(self):
        return '{0}: {1}. {2}'.format(self.holding, self.order, self.discount)


class ProductDiscountQuerySet(models.QuerySet):
    def eligible(self, person):
        return self.filter(discount__eligibilities__in=person.discount_eligibilities.all())

    def copy_to_holding_discounts(self, holding):
        for i in self:
            HoldingDiscount.objects.create(holding=holding, discount=i.discount, order=i.order)


@python_2_unicode_compatible
class ProductDiscount(models.Model):
    product = models.ForeignKey('Product', related_name='product_discounts', verbose_name=_('product'))
    discount = models.ForeignKey('Discount', related_name='product_discounts', verbose_name=_('discount'))

    order = models.PositiveIntegerField(verbose_name=_('order'))

    objects = ProductDiscountQuerySet.as_manager()

    class Meta:
        ordering = ('order',)
        unique_together = (('product', 'discount'),)

        verbose_name = _('product discount')
        verbose_name_plural = _('product discounts')

    def __str__(self):
        return '{0}: {1}. {2}'.format(self.product, self.order, self.discount)


class DiscountQuerySet(models.QuerySet):
    def eligible(self, person):
        self.filter(eligibilities__person=person)

    def map_eligibilities(self, person):
        for i in self:
            i.map_eligibility(person)


@python_2_unicode_compatible
class Discount(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id = models.PositiveIntegerField(verbose_name=_('object id'))
    object = GenericForeignKey('content_type', 'object_id')

    objects = DiscountQuerySet.as_manager()

    class Meta:
        unique_together = (('content_type', 'object_id'),)
        ordering = ('content_type', 'object_id')

        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self):
        return '{0}: {1}'.format(self.object._meta.verbose_name, self.object.__unicode__())

    def eligible(self, person):
        return self.object.eligible(person)

    def delta(self, price):
        return self.object.delta(price)

    def description(self):
        return self.object.description()

    def map_eligibility(self, person):
        if self.eligible(person):
            try:
                DiscountEligibility.objects.create(person=person, discount=self)
            except IntegrityError:
                # Everything's fine.
                pass
        else:
            try:
                DiscountEligibility.objects.get(person=person, discount=self).delete()
            except DiscountEligibility.DoesNotExist:
                # Everything's fine.
                pass

    def readable_discount(self):
        return self.object.readable_discount()

    def readable_discount_percent(self):
        return self.object.readable_discount_percent()


class BaseDiscount(models.Model):
    discount_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True,
                                          verbose_name=_('amount'))
    discount_percent = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                           verbose_name=_('percent'), help_text=_('Use decimal form, e.g. 0,25.'))

    class Meta:
        abstract = True

        verbose_name = _('base discount')
        verbose_name_plural = _('base discounts')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if (self.discount_amount and self.discount_percent) or (not self.discount_amount and not self.discount_percent):
            raise ValidationError(_("Please specify amount or percent."))

        super(BaseDiscount, self).save(force_insert, force_update, using, update_fields)

    def readable_discount(self):
        return self.readable_discount_percent() or '{0} kr'.format(self.discount_amount)

    def readable_discount_percent(self):
        if self.discount_percent:
            return format_percent(self.discount_percent)
        return ''

    def _percent_delta(self, price):
        return Decimal(price * self.discount_percent).quantize(Decimal('.01'))

    def eligible(self, person):
        """
        Method checking if the supplied person is eligible for this discount. Subclass this in your discount class and
        make it return True or False.
        """
        return None

    def delta(self, price):
        return self.discount_amount or self._percent_delta(price)

    def description(self):
        return self._meta.verbose_name


@python_2_unicode_compatible
class StudentUnionDiscount(BaseDiscount):
    student_union = models.ForeignKey('StudentUnion', related_name='discounts', verbose_name=_('student union'))

    class Meta:
        verbose_name = _('student union discount')
        verbose_name_plural = _('student union discounts')

    def __str__(self):
        return '{0}, {1}'.format(self.student_union, self.readable_discount())

    def eligible(self, person):
        return self.student_union.members.filter(liu_id=person.liu_id).exists()

    def description(self):
        return '{0}, {1}'.format(self._meta.verbose_name, self.student_union.name)


@python_2_unicode_compatible
class PersonalDiscount(BaseDiscount):
    people = models.ManyToManyField('tickle.Person', related_name='personal_discounts', verbose_name=_('people'))
    text = models.CharField(max_length=256, verbose_name=_('text'))

    class Meta:
        verbose_name = _('personal discount')
        verbose_name_plural = _('personal discounts')

    def __str__(self):
        return '{0} ({1}), {2}'.format(self.text, self.people.count(), self.readable_discount())

    def eligible(self, person):
        return self.people.filter(pk=person.pk).exists()

    def description(self):
        return self.text


class DiscountTeaser(models.Model):
    product = models.ForeignKey('Product', related_name='discount_teasers', verbose_name=('product'))
    text = models.TextField(verbose_name=_('text'))


