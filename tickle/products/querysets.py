from __future__ import absolute_import, unicode_literals

from decimal import Decimal

from django.db import models


class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)

    def holdings(self):
        from .models import Holding
        return Holding.objects.filter(product__in=self)


class HoldingQuerySet(models.QuerySet):
    # METHODS RETURNING HOLDING QUERYSETS #

    def deliverable(self):
        # todo: define further
        return self.purchased().undelivered()

    def delivered(self):
        # todo: extend for partial deliveries
        return self.filter(deliveries__isnull=False)

    def undelivered(self):
        # todo: extend for partial deliveries
        return self.filter(deliveries__isnull=True)

    def purchased(self):
        return self.filter(purchase__isnull=False)

    def unpurchased(self):
        return self.filter(purchase__isnull=True)

    # METHODS RETURNING OTHER QUERYSETS #

    def holders(self):
        return Person.objects.filter(holdings__in=self).distinct()

    # METHODS RETURNING NUMERIC VALUES #

    def total_cost(self):
        return self.annotate(price=models.Sum('product__price')).aggregate(models.Sum('price', field='price*quantity'))['price__sum']\
            or 0

    def discounted_total(self):
        total = Decimal("0.00")
        for i in self:
            total += i.discounted_total
        return total

    def quantity(self):
        return self.aggregate(models.Sum('quantity'))['quantity__sum'] or 0

    # METHODS MANIPULATING DATA #

    def remap_discounts(self):
        with atomic():
            for i in self:
                i.remap_discounts()
                i.invalidate_cached_discounts()


class CartQuerySet(models.QuerySet):
    def holdings(self):
        return Holding.objects.filter(cart__in=self)