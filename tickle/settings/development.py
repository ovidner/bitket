# -*- coding: utf-8 -*-
from . import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env.str('DJANGO_SECRET_KEY', 'dev')

SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', False)

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

INTERNAL_IPS = ('0.0.0.0',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel'
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    'SHOW_TOOLBAR_CALLBACK': lambda x: DEBUG,
}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
