# -*- coding: utf-8 -*-
from . import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env.str('DJANGO_SECRET_KEY', 'dev')

SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', False)
CORS_ORIGIN_ALLOW_ALL = env.bool('DJANGO_CORS_ORIGIN_ALLOW_ALL', True)
USE_X_FORWARDED_HOST = env.bool('DJANGO_USE_X_FORWARDED_HOST', False)

_EMAIL_CONFIG = env.email_url('DJANGO_EMAIL_URL', default='consolemail://')
EMAIL_BACKEND = _EMAIL_CONFIG.get('EMAIL_BACKEND')
EMAIL_HOST = _EMAIL_CONFIG.get('EMAIL_HOST')
EMAIL_HOST_USER = _EMAIL_CONFIG.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = _EMAIL_CONFIG.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = _EMAIL_CONFIG.get('EMAIL_PORT')
EMAIL_USE_TLS = _EMAIL_CONFIG.get('EMAIL_USE_TLS', True)

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
