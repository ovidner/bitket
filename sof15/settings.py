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


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'debug_toolbar',

    'liu.django',
    'guardian',
    'raven.contrib.django.raven_compat',
    'crispy_forms',

    'tickle',
    'orchard',
    #'fungus',
    'karthago',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
)

ROOT_URLCONF = 'sof15.urls'

WSGI_APPLICATION = 'sof15.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'liu.django.backends.LiUStudentBackend',
    'guardian.backends.ObjectPermissionBackend',
)

AUTH_USER_MODEL = 'tickle.TickleUser'

ANONYMOUS_USER_ID = -1

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

# Breaking the 12 factor rules here. Don't have the time.
# todo: 12factorise
SERVER_EMAIL = 'tickle@sof15.se'
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'olle.vidner@sof15.se'
EMAIL_HOST_PASSWORD = 'tDpIHwRrlJW5Tg32GZbhmA'

ADMINS = (
    ('Olle Vidner', 'olle.vidner@sof15.se'),
    ('Victor Karlsson Sehlin', 'victor.karlsson.sehlin@sof15.se'),
    ('Gustav Häger', 'hager.gustav@gmail.com'),
)

RAVEN_CONFIG = {
    'dsn': 'https://c2b3bbede63d445c94336de8b0de8419:2b09bb511528494580929f1353e300eb@app.getsentry.com/36275',
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