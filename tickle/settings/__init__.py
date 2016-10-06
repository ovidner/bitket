# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import os
import warnings

from django.core.urlresolvers import reverse_lazy

import environ
import raven
import stripe

from tickle.people.saml.constants import claims

env = environ.Env()

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('tickle')

# https://docs.python.org/3/library/warnings.html#temporarily-suppressing-warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    env.read_env(str(ROOT_DIR.path('.env')))

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'djangosecure',
    'gunicorn',
    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    'dry_rest_permissions',
    'raven.contrib.django.raven_compat',
    'django_extensions',
    'opbeat.contrib.django',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'tickle.common',
    'tickle.common.celery',
    'tickle.conditions',
    'tickle.events',
    'tickle.modifiers',
    'tickle.organizers',
    'tickle.payments',
    'tickle.people',
    'tickle.people.saml',
    'tickle.products',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'opbeat.contrib.django.middleware.Opbeat404CatchMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'tickle.contrib.sites.migrations'
}

ALLOWED_HOSTS = ["*"]

SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env.str('DJANGO_EMAIL_BACKEND',
                        'django_mailgun.MailgunBackend')
DEFAULT_FROM_EMAIL = env.str('DJANGO_DEFAULT_FROM_EMAIL',
                             'liubiljett.se <info@liubiljett.se>')
EMAIL_SUBJECT_PREFIX = env.str('DJANGO_EMAIL_SUBJECT_PREFIX',
                               '[liubiljett.se] ')
SERVER_EMAIL = env.str('DJANGO_SERVER_EMAIL', DEFAULT_FROM_EMAIL)
MAILGUN_ACCESS_KEY = env.str('MAILGUN_ACCESS_KEY', '')
MAILGUN_SERVER_NAME = env.str('MAILGUN_SERVER_NAME', '')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""liubiljett.se admin""", address)
          for address in env('DJANGO_ADMINS', list, ['admin@liubiljett.se'])]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env.str('DJANGO_REDIS_URL'),
        'OPTIONS': {
            "CLIENT_CLASS": 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Stockholm'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'sv-se'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': None,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

if env.bool('DJANGO_CACHE_TEMPLATES', True):
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
    ]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: http://whitenoise.evans.io/en/latest/django.html#cdn
STATIC_HOST = env.str('DJANGO_STATIC_HOST', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = STATIC_HOST + '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'tickle.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'tickle.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'tickle.people.saml.backends.LiuAdfsBackend',
)

# Some really nice defaults
ACCOUNT_ADAPTER = 'tickle.people.adapters.AccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_ADAPTER = 'tickle.people.adapters.SocialAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'people.Person'
LOGIN_REDIRECT_URL = reverse_lazy('client:home')
#LOGIN_URL = 'account_login'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    )
}

# SLUGIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# Sentry Configuration
# SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT')
SENTRY_CELERY_LOGLEVEL = env.str('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
RAVEN_CONFIG = {
    'dsn': env.str('DJANGO_SENTRY_DSN', 'https://a:b@dummydsn.com/1'),
    'release': raven.fetch_git_sha(str(ROOT_DIR)),
    'CELERY_LOGLEVEL': env.str('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
}

OPBEAT = {
    'ORGANIZATION_ID': env.str('DJANGO_OPBEAT_ORGANIZATION_ID', ''),
    'APP_ID': env.str('DJANGO_OPBEAT_APP_ID', ''),
    'SECRET_TOKEN': env.str('DJANGO_OPBEAT_SECRET_TOKEN', ''),
    'DEBUG': True
}

GOOGLE_ANALYTICS_ID = env.str('GOOGLE_ANALYTICS_ID', '')

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    # This is THE log config. This makes sense since we use a root logger.
    'disable_existing_loggers': True,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
        },
        # Used by the Django development server. Included from django.utils.log.
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        # Used by the Django development server. Included from django.utils.log.
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'opbeat': {
            'level': 'WARNING',
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        }
    },
    'loggers': {
        # Log everything of level WARNING or above to the console and to opbeat.
        # This is to keep the log config as simple and as predictable as
        # possible.
        None: {
            'level': 'WARNING',
            'handlers': ['console', 'opbeat']
        },
        # Exceptions to the above rule go here. Use propagate=False to prevent
        # the root logger to also swallow the event.

        # Used by the Django development server. Included from django.utils.log.
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

KOBRA_USER = env.str('KOBRA_USER', '')
KOBRA_KEY = env.str('KOBRA_KEY', '')

STRIPE_OAUTH_AUTHORIZE_URL = 'https://connect.stripe.com/oauth/authorize'
STRIPE_OAUTH_TOKEN_URL = 'https://connect.stripe.com/oauth/token'
STRIPE_OAUTH_SIGN_MAX_AGE = 5 * 60
STRIPE_PUBLIC_KEY = env.str('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = env.str('STRIPE_SECRET_KEY', '')
STRIPE_CLIENT_ID = env.str('STRIPE_CLIENT_ID', '')
stripe.api_key = STRIPE_SECRET_KEY

CURRENCY = 'SEK'

CACHE_TIMEOUT_PERSON_CONDITIONS = 10 * 60

SAML_SP_CERT = env.str('SAML_SP_CERT', '')
SAML_SP_KEY = env.str('SAML_SP_KEY', '')
SAML_SP_ACS_URL = env.str('SAML_SP_ACS_URL',
                          'https://www.liubiljett.se/_saml/login/complete/')
SAML_SP_SLO_URL = env.str('SAML_SP_SLO_URL',
                          'https://www.liubiljett.se/_saml/logout/')
SAML_DEBUG = env.bool('SAML_DEBUG', False)
SAML_STRICT = env.bool('SAML_STRICT', True)
SAML_USER_ATTRIBUTE_MAPPINGS = {
    'email': claims.CLAIM_EMAIL,
    'first_name': claims.CLAIM_GIVEN_NAME,
    'last_name': claims.CLAIM_SURNAME,
}
