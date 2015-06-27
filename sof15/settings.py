# -*- coding: utf-8 -*-
"""
Django settings for sof15 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from __future__ import unicode_literals
import os
from six import text_type

from django.utils.translation import ugettext_lazy as _

import environ


env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=text_type,
    ALLOWED_HOSTS=(list, []),
    KOBRA_USER=text_type,
    KOBRA_API_KEY=text_type,
    SENTRY_DSN=text_type,
    MANDRILL_API_KEY=text_type
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEV_ENV = os.path.join(BASE_DIR, 'dev.env')

# If there is a dev.env file, we go into developer mode
if os.path.isfile(DEV_ENV):
    # Reads the DEV_ENV file and sets any variables defined there.
    env.read_env(DEV_ENV)

    # Sets some sane defaults suitable for development IF these are not already
    # set by environmental variables or the env file.
    os.environ.setdefault('DEBUG', 'true')
    os.environ.setdefault('SECRET_KEY', 'dev')
    os.environ.setdefault('DATABASE_URL', 'sqlite:///db.sqlite3')
    os.environ.setdefault('CACHE_URL', 'locmemcache://')
    os.environ.setdefault('KOBRA_USER', '')
    os.environ.setdefault('KOBRA_API_KEY', '')
    os.environ.setdefault('SENTRY_DSN', '')
    os.environ.setdefault('MANDRILL_API_KEY', '')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Public URL to the system root, without trailing slash.
PRIMARY_HOST = 'https://tickle.sof15.se'

# Application definition

INSTALLED_APPS = (
    'suit',  # Must be installed before `django.contrib.admin`
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'debug_toolbar',
    'djrill',
    'guardian',
    'raven.contrib.django.raven_compat',
    'crispy_forms',
    'rest_framework',
    'markdown_deux',

    'tickle',
    'orchard',
    'fungus',
    'karthago',
    'invar',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.template.context_processors.request',
)

SUIT_CONFIG = {
    'ADMIN_NAME': 'Tickle SOF15',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoObjectPermissions',
    ),
}

# Database backed cache backend.
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Session timeout is 6 hours
SESSION_COOKIE_AGE = 60 * 60 * 6

ROOT_URLCONF = 'sof15.urls'

WSGI_APPLICATION = 'sof15.wsgi.application'

AUTHENTICATION_BACKENDS = (
    # Adding the standard ModelBackend here potentially means a huge security risk, don't do it!
    'tickle.auth.backends.TickleBackend',  # Handles email auth
    'tickle.auth.backends.LiUStudentLDAPBackend',
    # 'tickle.auth.backends.LiUEmployeeLDAPBackend',
    'guardian.backends.ObjectPermissionBackend',
)

AUTH_USER_MODEL = 'tickle.TickleUser'

ANONYMOUS_USER_ID = -1
GUARDIAN_GET_INIT_ANONYMOUS_USER = 'tickle.models.get_init_anonymous_user'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'profile'

if not DEBUG:
    # Disabled due to redirect loop in combination with CloudFlare
    # SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# WARNING: This setting assumes a correctly set up proxy.
# See https://docs.djangoproject.com/en/1.7/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': env.db()
}
DATABASES['default']['CONN_MAX_AGE'] = 60

CACHES = {
    'default': env.cache()
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'sv-se'

LANGUAGES = (
    ('sv', _('Swedish')),
    ('en', _('English')),
)

DATE_FORMAT = "Y-m-d"
DATETIME_FORMAT = "Y-m-d H:i"

TIME_ZONE = 'Europe/Stockholm'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'sof15', 'locale'),

    os.path.join(BASE_DIR, 'tickle', 'locale'),
    os.path.join(BASE_DIR, 'fungus', 'locale'),
    os.path.join(BASE_DIR, 'invar', 'locale'),
    os.path.join(BASE_DIR, 'karthago', 'locale'),
    os.path.join(BASE_DIR, 'orchard', 'locale'),
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

KOBRA_USER = env('KOBRA_USER')
KOBRA_KEY = env('KOBRA_API_KEY')

SERVER_EMAIL = 'Tickle SOF15 <tickle@sof15.se>'
DEFAULT_FROM_EMAIL = 'Tickle SOF15 <tickle@sof15.se>'

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
MANDRILL_API_KEY = env('MANDRILL_API_KEY')

ADMINS = (
    ('Olle Vidner', 'olle.vidner@sof15.se'),
    ('Victor Karlsson Sehlin', 'victor.karlsson.sehlin@sof15.se'),
    ('Gustav Häger', 'hager.gustav@gmail.com'),
)

RAVEN_CONFIG = {
    'dsn': env('SENTRY_DSN')
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

INVAR_OCR_CHECK_LENGTH = 2
INVAR_BG = '5415-8712'
INVAR_IBAN = 'SE48 1200 0000 0131 6018 5524'
INVAR_BIC_SWIFT = 'DABASESX'
INVAR_DUE_DAYS = 14
INVAR_BGMAX_TIMEZONE = 'Europe/Stockholm'
