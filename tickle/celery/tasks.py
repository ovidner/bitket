from __future__ import (absolute_import, print_function, unicode_literals)

from .apps import celery


@celery.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

