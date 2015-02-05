# -*- coding: utf-8 -*-
from django.apps import AppConfig


class TickleConfig(AppConfig):
    name = 'tickle'
    verbose_name = 'Tickle'

    def ready(self):
        """
        Defines signals and connects receivers.
        """
        import tickle.receivers