from __future__ import absolute_import, unicode_literals
import logging
logger = logging.getLogger(__name__)

from django.db import models

from tickle import products, people, events


class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)

    def holdings(self):
        from .models import Holding
        return Holding.objects.filter(products__in=self)

    def events(self):
        return events.models.MainEvent.objects.filter(products__in = self).distinct()


class HoldingQuerySet(models.QuerySet):
    # METHODS RETURNING HOLDING QUERYSETS #

    def purchased(self):
        return self.filter(cart__purchased__isnull=False)

    def unpurchased(self):
        return self.filter(cart__purchased__isnull=True)

    def organized_by(self, organizer):
        return self.filter(product__main_event__organizer = organizer)

    # METHODS RETURNING OTHER QUERYSETS #

    def holders(self):
        return people.models.Person.objects.filter(holdings__in=self).distinct()

    def products(self):
        return products.models.Product.objects.filter(holdings__in=self).distinct()

    # METHODS RETURNING NUMERIC VALUES #

    def total_cost(self):
        return self.annotate(price=models.Sum('product__price')).aggregate(models.Sum('price', field='price*quantity'))['price__sum']\
            or 0

    def quantity(self):
        return self.aggregate(models.Sum('quantity'))['quantity__sum'] or 0

    def prepare_for_purchase(self, ignore_limits=False, modify_history_allowed=False):
        for i in self:
            i.prepare_for_purchase(
                ignore_limits=ignore_limits,
                modify_history_allowed=modify_history_allowed)

    def email_ticket(self):
        for i in self:
            i.email_ticket()


class CartQuerySet(models.QuerySet):
    def purchased(self):
        return self.filter(purchased__isnull=False)

    def unpurchased(self):
        return self.filter(purchased__isnull=True)

    def holdings(self):
        return products.models.Holding.objects.filter(cart__in=self)
