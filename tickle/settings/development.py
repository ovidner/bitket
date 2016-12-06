# -*- coding: utf-8 -*-
from . import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env.str('DJANGO_SECRET_KEY', 'dev')

SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', False)
CORS_ORIGIN_ALLOW_ALL = env.bool('DJANGO_CORS_ORIGIN_ALLOW_ALL', True)

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
