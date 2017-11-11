# -*- coding: utf-8 -*-
import warnings
import datetime
from os import path

import certifi
from django.core.urlresolvers import reverse_lazy
import psycopg2
import stripe
import sesam

from .utils.settings import PrefixEnv


env = PrefixEnv(prefix='BITKET_')

# Build paths inside the project like this: path.join(ROOT_DIR, ...)
ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))  # /backend
APPS_DIR = path.join(ROOT_DIR, 'bitket')  # /backend/bitket
ENV_FILE = path.join(ROOT_DIR, env.str('ENV_FILE', default='.env'))

# Ignores warnings if .env does not exist
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    env.read_env(ENV_FILE)

DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env.str('SECRET_KEY')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',

    'corsheaders',
    'djangosecure',
    'gunicorn',
    'rest_framework',
    'social.apps.django_app.default',
    'rest_social_auth',
    'django_extensions',
    'opbeat.contrib.django',

    'bitket',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'opbeat.contrib.django.middleware.Opbeat404CatchMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)
CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL', False)
USE_X_FORWARDED_HOST = env.bool('USE_X_FORWARDED_HOST', True)

SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

_EMAIL_CONFIG = env.email_url('EMAIL_URL')
EMAIL_BACKEND = _EMAIL_CONFIG.get('EMAIL_BACKEND')
EMAIL_HOST = _EMAIL_CONFIG.get('EMAIL_HOST')
EMAIL_HOST_USER = _EMAIL_CONFIG.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = _EMAIL_CONFIG.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = _EMAIL_CONFIG.get('EMAIL_PORT')
EMAIL_USE_TLS = _EMAIL_CONFIG.get('EMAIL_USE_TLS', True)
DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL',
                             'Bitket <hello@bitket.se>')
EMAIL_SUBJECT_ENV_PREFIX = env.str('EMAIL_SUBJECT_ENV_PREFIX',
                               '[Bitket] ')
SERVER_EMAIL = env.str('SERVER_EMAIL', DEFAULT_FROM_EMAIL)

ADMINS = tuple(
    ("""Bitket admin""", address)
    for address in
    env.list('ADMINS', default=('admin@bitket.se',))
)

MANAGERS = ADMINS

# BACKING SERVICES
# ----------------
DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES['default']['CONN_MAX_AGE'] = 500

REDIS_URL = env.url('REDIS_URL')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': str(REDIS_URL),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


TIME_ZONE = 'Europe/Stockholm'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(APPS_DIR, 'templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

if env.bool('CACHE_TEMPLATES', True):
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
    ]


STATIC_URL = '/static/'
STATIC_ROOT = path.join(ROOT_DIR, 'collected-static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'bitket.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'bitket.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_liu.LiuBackend',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2'
)

# fullname is the identifier used by python-social-auth.
SOCIAL_AUTH_USER_FIELDS = ['email', 'fullname']
SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Associates the current social details with another user account with
    # a similar email address.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Gets student union, if applicable
    'bitket.models.social_get_union',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',
)

SOCIAL_AUTH_FACEBOOK_KEY = env.str('AUTH_FACEBOOK_CLIENT_ID', '')
SOCIAL_AUTH_FACEBOOK_SECRET = env.str('AUTH_FACEBOOK_CLIENT_SECRET', '')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'en_US',
    'fields': 'id, name, email'
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str('AUTH_GOOGLE_CLIENT_ID', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str('AUTH_GOOGLE_CLIENT_SECRET', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
# https://github.com/certifi/python-certifi/issues/32
SOCIAL_AUTH_GOOGLE_OAUTH2_VERIFY_SSL = certifi.old_where()

SOCIAL_AUTH_LIU_HOST = env.str('AUTH_LIU_HOST', default='fs.liu.se')
SOCIAL_AUTH_LIU_KEY = env.str('AUTH_LIU_CLIENT_ID', '')
SOCIAL_AUTH_LIU_SCOPE = env.list('AUTH_LIU_RESOURCE', default=[])
SOCIAL_AUTH_LIU_VERIFY_IAT = env.bool('AUTH_LIU_VERIFY_IAT', default=True)
SOCIAL_AUTH_LIU_VERIFY_SSL = env.bool('AUTH_LIU_VERIFY_SSL', default=True)
SOCIAL_AUTH_LIU_X509_CERT = env.str('AUTH_LIU_X509_CERT', default=None)

AUTH_USER_MODEL = 'bitket.User'
LOGIN_REDIRECT_URL = reverse_lazy('client:home')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    )
}
JWT_AUTH = {
    'JWT_ALGORITHM': 'HS512',
    'JWT_ALLOW_REFRESH': True,
    'JWT_PAYLOAD_HANDLER': 'bitket.serializers.jwt_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
}

# SLUGIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

OPBEAT = {
    'ORGANIZATION_ID': env.str('OPBEAT_ORGANIZATION_ID', ''),
    'APP_ID': env.str('OPBEAT_APP_ID', ''),
    'SECRET_TOKEN': env.str('OPBEAT_SECRET_TOKEN', '')
}

GOOGLE_ANALYTICS_ID = env.str('GOOGLE_ANALYTICS_ID', '')

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

KOBRA_HOST = env.str('KOBRA_HOST', default='https://kobra.karservice.se')
KOBRA_TOKEN = env.str('KOBRA_TOKEN', default='')

SESAM_USERNAME = env.str('SESAM_USERNAME', default='')
SESAM_PASSWORD = env.str('SESAM_PASSWORD', default='')
SESAM_STUDENT_SERVICE_CLIENT = sesam.SesamStudentServiceClient(
    username=SESAM_USERNAME,
    password=SESAM_PASSWORD
)

STRIPE_OAUTH_AUTHORIZE_URL = 'https://connect.stripe.com/oauth/authorize'
STRIPE_OAUTH_TOKEN_URL = 'https://connect.stripe.com/oauth/token'
STRIPE_OAUTH_SIGN_MAX_AGE = 5 * 60
STRIPE_PUBLIC_KEY = env.str('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = env.str('STRIPE_SECRET_KEY', '')
STRIPE_CLIENT_ID = env.str('STRIPE_CLIENT_ID', '')
stripe.api_key = STRIPE_SECRET_KEY

CURRENCY = 'SEK'

CACHE_TIMEOUT_PERSON_CONDITIONS = 10 * 60