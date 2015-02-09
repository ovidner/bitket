# -*- coding: utf-8 -*-
"""
Django settings for sof15 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import django12factor
d12f = django12factor.factorise(
    custom_settings=[
        'KOBRA_USER',
        'KOBRA_API_KEY',
        'SENTRY_DSN',
        'MANDRILL_API_KEY',
    ]
)

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = d12f['SECRET_KEY']
# SECRET_KEY = 'wu*4qyzkc9r5at0j=8qqz&)yjuq&kze_ip71khzdfv0g(^(m-_'

DEBUG = d12f['DEBUG']

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = d12f['ALLOWED_HOSTS']

# URL to the system.
PRIMARY_HOST = 'tickle.sof15.se'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'djangosecure',
    'debug_toolbar',
    'djrill',
    'guardian',
    'raven.contrib.django.raven_compat',
    'crispy_forms',

    'liu.django',

    'tickle',
    'orchard',
    'fungus',
    'karthago',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',

    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.cache.FetchFromCacheMiddleware',
)

# Database backed cache backend.
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

ROOT_URLCONF = 'sof15.urls'

WSGI_APPLICATION = 'sof15.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'liu.django.backends.LiUStudentBackend',  # Temporarily activated until we allow LiU id logins.
    'guardian.backends.ObjectPermissionBackend',
)

AUTH_USER_MODEL = 'tickle.TickleUser'

ANONYMOUS_USER_ID = -1

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# WARNING: This setting assumes a correctly set up proxy.
# See https://docs.djangoproject.com/en/1.7/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = d12f['DATABASES']
CACHES = d12f['CACHES']

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'sv-se'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('sv', _('Swedish')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, '_conf', 'locale'),

    os.path.join(BASE_DIR, 'tickle', 'locale'),
    os.path.join(BASE_DIR, 'orchard', 'locale'),
    os.path.join(BASE_DIR, 'karthago', 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '_build', 'static')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'sof15', 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'sof15', 'templates'),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LIU_KOBRA_USER = d12f['KOBRA_USER']
LIU_KOBRA_API_KEY = d12f['KOBRA_API_KEY']

SERVER_EMAIL = 'tickle@sof15.se'
DEFAULT_FROM_EMAIL = 'Tickle SOF15 <tickle@sof15.se>'

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
MANDRILL_API_KEY = d12f['MANDRILL_API_KEY']


ADMINS = (
    ('Olle Vidner', 'olle.vidner@sof15.se'),
    ('Victor Karlsson Sehlin', 'victor.karlsson.sehlin@sof15.se'),
    ('Gustav Häger', 'hager.gustav@gmail.com'),
)

RAVEN_CONFIG = {
    'dsn': d12f['SENTRY_DSN'],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': True,
        },
    },
}