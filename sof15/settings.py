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

LIU_KOBRA_USER = 'sof15'
LIU_KOBRA_API_KEY = '13bbfc68cacb9119db5a'

RAVEN_CONFIG = {
    'dsn': 'http://84863b989a8b43408184cc6074004fa2:d26e02ebdee549d7ac6aa3b42f83d5d2@dale.sof15.se:9000/2',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
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
            'level': 'DEBUG',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True,
            },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
            },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
            },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
            },
        'liu.django': {
            'level': 'DEBUG',
            'handlers': ['sentry'],
            'propagate': False,
            },
        },
    }