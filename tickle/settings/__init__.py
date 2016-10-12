# -*- coding: utf-8 -*-
import warnings

from django.core.urlresolvers import reverse_lazy
import environ
import stripe

env = environ.Env()

ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('tickle')

# https://docs.python.org/3/library/warnings.html#temporarily-suppressing-warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    env.read_env(str(ROOT_DIR.path('.env')))

# APP CONFIGURATION
# ------------------------------------------------------------------------------
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',

    'djangosecure',
    'gunicorn',
    'rest_framework',
    'social.apps.django_app.default',
    'rest_social_auth',
    'dry_rest_permissions',
    'django_extensions',
    'opbeat.contrib.django',

    'tickle',
    'tickle.celery',
)

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
    'social.backends.facebook.FacebookOAuth2',
    'tickle.adfs.ADFSOAuth2'
)

SOCIAL_AUTH_USER_FIELDS = ['email', 'first_name', 'last_name']

SOCIAL_AUTH_ADFS_HOST = 'adfs.lab.vidnet.io'
SOCIAL_AUTH_ADFS_KEY = env.str('ADFS_CLIENT_ID', '')
SOCIAL_AUTH_ADFS_SCOPE = ['https://www.liubiljett.se']
SOCIAL_AUTH_ADFS_X509_CERT = env.str('ADFS_X509_CERT', '')

SOCIAL_AUTH_FACEBOOK_KEY = env.str('FACEBOOK_CLIENT_ID', '')
SOCIAL_AUTH_FACEBOOK_SECRET = env.str('FACEBOOK_CLIENT_SECRET', '')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

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
