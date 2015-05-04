# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.signals import user_logged_in

from .models import TickleUser, Person, Discount, Holding, ShoppingCart


@receiver(user_logged_in)
def map_discount_eligibilities(sender, **kwargs):
    person = kwargs['user'].person
    Discount.objects.map_eligibilities(person)


@receiver(user_logged_in)
def create_shopping_cart(sender, **kwargs):
    person = kwargs['user'].person
    ShoppingCart.objects.get_or_create(person=person)


@receiver(post_save, sender=Holding)
def send_ticket(sender, instance, **kwargs):
    # Don't do anything if called by `loaddata` etc.
    if kwargs['raw']:
        return

    if instance.product.is_ticket_type and instance.purchase:
        instance.send_ticket()
