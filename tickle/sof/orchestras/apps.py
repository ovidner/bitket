# -*- coding: utf-8 -*-
from django.apps import AppConfig


class OrchardConfig(AppConfig):
    name = 'orchard'
    verbose_name = 'Orchard'

    def ready(self):
        """
        Defines signals and connects receivers.
        """
