# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import pre_save

from .models.people import TickleUser, Person


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
