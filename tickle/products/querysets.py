from __future__ import absolute_import, unicode_literals
import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.conf import settings
from django.db import models

import stripe

from tickle import products, people, events
from tickle.payments.models import Transaction


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


    def purchased_total_cost(self):
        return self.annotate(price=models.Sum('purchase_price')).aggregate(models.Sum('price', field='price*quantity'))['price__sum'] or 0


    def prepare_for_purchase(self):
        for i in self:
            i.prepare_for_purchase()

    def charge(self, person, stripe_token):
        stripe_customer = stripe.Customer.create(
            source=stripe_token,
            description=person.get_full_name(),
            email=person.email,
            metadata={'liubiljett_person_id': person.pk}
        )
        completed_charges = []
        try:
            for organizer in self.products().events().organizers():
                charge_amount = self.organized_by(organizer).purchased_total_cost()

                charge = stripe.Charge.create(
                    customer=stripe_customer,
                    amount=int(charge_amount*100), #Convert price from kr to ore.
                    currency=settings.CURRENCY,
                    destination=organizer.stripe_account_id
                )
                if charge.status == "succeeded":
                    completed_charges.append(charge)
                    Transaction.objects.create(amount=charge_amount, stripe_charge=charge.id)
        except stripe.error.CardError as e:
            # The payment to the current organizer has failed.
            # Roll back the database transaction.
            logger.exception("A charge failed.")
            for charge in completed_charges:
                try:
                    stripe.Refund.create(charge=charge.id)
                except stripe.error.StripeError:
                    logger.exception("An error occured while refunding charges.")
            raise e
        finally:
            stripe_customer.delete()




class CartQuerySet(models.QuerySet):
    def purchased(self):
        return self.filter(purchased__isnull=False)

    def unpurchased(self):
        return self.filter(purchased__isnull=True)

    def holdings(self):
        return products.models.Holding.objects.filter(cart__in=self)
