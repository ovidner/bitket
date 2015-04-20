# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.signals import user_logged_in

from .models import TickleUser, Person, Discount, Holding, ShoppingCart


@receiver(pre_save, sender=TickleUser)
def generate_and_send_password_user(sender, instance, **kwargs):
    # Do this only for non-LiU id users.
    if not instance.person.liu_id and not instance.password and instance.id != settings.ANONYMOUS_USER_ID:
        instance.generate_and_send_password()


@receiver(pre_save, sender=Person)
def generate_and_send_password_person(sender, instance, **kwargs):
    # Do this only for non-LiU id users.
    if not instance.liu_id and hasattr(instance, 'user') and not instance.user.password and instance.id != settings.ANONYMOUS_USER_ID:
        instance.user.generate_and_send_password()


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
    print('hej')
    if instance.product.is_ticket_type and getattr(instance, 'purchase'):
        instance.send_ticket()
