# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

from django.dispatch import receiver

from django_auth_ldap.backend import populate_user

from liu.django.backends import LiUStudentBackend


@receiver(populate_user, sender=LiUStudentBackend)
def populate_liu_id(sender, **kwargs):
    logger.debug(kwargs.get('ldap_user'))