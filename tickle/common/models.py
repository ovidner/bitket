from __future__ import absolute_import, unicode_literals

from django.db import models


class TickleModel(models.Model):
    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super(TickleModel, self).save(force_insert, force_update, using,
                                      update_fields)
