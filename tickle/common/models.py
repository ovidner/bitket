from __future__ import absolute_import, unicode_literals

import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import allow_staff_or_superuser


class Model(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'))

    class Meta:
        abstract = True

    @staticmethod
    def has_read_permission(request):
        # Use this method only to explicitly deny permissions.
        return True

    @staticmethod
    def has_write_permission(request):
        # Use this method only to explicitly deny permissions.
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_create_permission(request):
        return False

    def has_object_read_permission(self, request):
        return True

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_object_destroy_permission(self, request):
        # Explicitly defined. No object should be user removable by default.
        return False
