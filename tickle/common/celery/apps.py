from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os

from django.apps import AppConfig
from django.conf import settings

from celery import Celery

celery = Celery('tickle')


class CeleryConfig(AppConfig):
    name = 'tickle.common.celery'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        celery.config_from_object('django.conf:settings')
        celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
