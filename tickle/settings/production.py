# -*- coding: utf-8 -*-
from . import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', False)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env.str('DJANGO_SECRET_KEY')

SESSION_COOKIE_SECURE = env.bool('DJANGO_SESSION_COOKIE_SECURE', True)
CORS_ORIGIN_ALLOW_ALL = env.bool('DJANGO_CORS_ORIGIN_ALLOW_ALL', False)
