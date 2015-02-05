# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

from django.dispatch import receiver

from django_auth_ldap.backend import populate_user
from django.db.models.signals import pre_save, post_save

from liu.django.backends import LiUStudentBackend
from guardian.shortcuts import assign_perm

from .models.people import TickleUser, Person


@receiver(populate_user, sender=LiUStudentBackend)
def populate_liu_id(sender, **kwargs):
    logger.debug(kwargs.get('ldap_user'))


@receiver(pre_save, sender=TickleUser)
def generate_and_send_password_user(sender, instance, **kwargs):
    if not instance.password:
        instance.generate_and_send_password()


@receiver(pre_save, sender=Person)
def generate_and_send_password_person(sender, instance, **kwargs):
    if hasattr(instance, 'user') and not instance.user.password:
        instance.user.generate_and_send_password()


@receiver(post_save)
def assign_view_person_perm(sender, instance, **kwargs):
    if isinstance(instance, TickleUser):
        assign_perm('view_person', instance, instance.person)
    if isinstance(instance, Person) and hasattr(instance, 'user'):
        assign_perm('view_person', instance.user, instance)