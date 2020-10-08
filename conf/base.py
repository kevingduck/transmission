"""
Django settings for transmission project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import json
import os
import sys
from urllib.parse import urlparse

import environ

ENV = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Versions for engine subscription
LOAD_VERSION = '1.1.0'
SHIPTOKEN_VERSION = '1.0.0'

GTX_VALIDATION_URL = 'https://shipchain.acm.gtxcorp.net/validate'
ENGINE_RPC_URL = os.environ.get('ENGINE_RPC_URL', "http://engine-rpc:2000/")
INTERNAL_URL = os.environ.get('INTERNAL_URL', 'http://transmission-runserver:8000')
PROFILES_URL = os.environ.get('PROFILES_URL')
PROFILES_ENABLED = PROFILES_URL != 'DISABLED'
if PROFILES_URL != 'DISABLED':
    PROFILES_URL = ('http://profiles-runserver:8000' if ('runserver' in INTERNAL_URL)
                    else INTERNAL_URL.replace("transmission", "profiles"))

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', None)

ENVIRONMENT = os.environ.get('ENV', 'LOCAL')
SERVICE = os.environ.get('SERVICE', 'NONE')
PROJECT_MODULE = 'transmission'

MANAGE_PY_COMMAND = None

RELOAD_SERVER = False
if len(sys.argv) > 1 and sys.argv[0] == 'manage.py':
    MANAGE_PY_COMMAND = sys.argv[1]
    RELOAD_SERVER = (os.environ.get('RUN_MAIN') != 'true')

SUBSCRIBE_EVENTS = (ENVIRONMENT != 'TEST' and
                    MANAGE_PY_COMMAND != 'migrate' and
                    MANAGE_PY_COMMAND != 'test' and
                    not RELOAD_SERVER)

ALLOWED_HOSTS = ['*']

CSRF_USE_SESSIONS = True

CORS_ORIGIN_ALLOW_ALL = True

BOTO3_SESSION = None

if ENVIRONMENT in ('PROD', 'DEMO', 'STAGE', 'DEV'):
    if ENVIRONMENT == 'PROD':
        DEBUG = False
        LOG_LEVEL = 'INFO'
        FRONTEND_DOMAIN = 'portal.shipchain.io'
    elif ENVIRONMENT == 'DEMO':
        DEBUG = False
        LOG_LEVEL = 'INFO'
        FRONTEND_DOMAIN = 'demo.shipchain.io'
    else:
        DEBUG = os.environ.get('FORCE_DEBUG', False)
        LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
        FRONTEND_DOMAIN = f'portal-{ENVIRONMENT.lower()}.shipchain.io'

    import boto3
    BOTO3_SESSION = boto3.Session(region_name='us-east-1')
    SECRETS_MANAGER = BOTO3_SESSION.client('secretsmanager')

    SECRET_KEY = json.loads(SECRETS_MANAGER.get_secret_value(
        SecretId=f'TRANSMISSION_SECRET_KEY_{ENVIRONMENT}'
    )['SecretString'])['SECRET_KEY']

    RDS_CREDS = json.loads(SECRETS_MANAGER.get_secret_value(
        SecretId=f'TRANSMISSION_RDS_{ENVIRONMENT}'
    )['SecretString'])

    os.environ['DATABASE_URL'] = (f'postgis://{RDS_CREDS["username"]}:{RDS_CREDS["password"]}@'
                                  f'{RDS_CREDS["host"]}:{RDS_CREDS["port"]}/{RDS_CREDS["dbname"]}')

    os.environ['EMAIL_URL'] = json.loads(SECRETS_MANAGER.get_secret_value(
        SecretId=f'TRANSMISSION_EMAIL_URL_{ENVIRONMENT}'
    )['SecretString'])['EMAIL_URL']

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    URL_SHORTENER_HOST = 't.shipchain.io'
    URL_SHORTENER_URL = f'https://{URL_SHORTENER_HOST}/'

else:
    DEBUG = os.environ.get('FORCE_DEBUG', True)
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    DEV_SECRET_KEY = 'devsecretkey' * 19  # noqa
    SECRET_KEY = os.environ.get('SECRET_KEY', DEV_SECRET_KEY)
    FRONTEND_DOMAIN = 'localhost:3000'
    URL_SHORTENER_HOST = 'fglcol31yk.execute-api.us-east-1.amazonaws.com'
    URL_SHORTENER_URL = f'https://{URL_SHORTENER_HOST}/test'
    POSTGIS_VERSION = (2, 4, 4)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fullurl',
    'django.contrib.gis',
    'django_extensions',
    'django_filters',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_serializer_field_permissions',
    'influxdb_metrics',
    'corsheaders',
    'apps.jobs',
    'apps.eth',
    'apps.shipments',
    'apps.schema',
    'apps.documents',
    'apps.imports',
    'apps.routes',
    'channels',
    'simple_history',
    'rangefilter',
]
if DEBUG and ENV in ('LOCAL', 'TEST',) and not MANAGE_PY_COMMAND:
    INSTALLED_APPS += ['django_pycharm_breakpoint']

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'EXCEPTION_HANDLER': 'shipchain_common.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'shipchain_common.pagination.JsonApiPagePagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'apps.throttling.MonthlyRateThrottle',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'COERCE_DECIMAL_TO_STRING': False,
}

if PROFILES_URL:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
        'rest_framework_simplejwt.authentication.JWTTokenUserAuthentication',
    )
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = (
        'rest_framework.permissions.IsAuthenticated',
    )

MIDDLEWARE = [
    'influxdb_metrics.middleware.InfluxDBRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'shipchain_common.custom_logging.middleware.UserOrganizationMiddleware',
]

ROOT_URLCONF = 'apps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'apps/shipments/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'apps.wsgi.application'
ASGI_APPLICATION = 'apps.routing.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': ENV.db(default='postgis://transmission:transmission@psql:5432/transmission'),
}

# Caching
CACHES = {
    'default': ENV.cache('REDIS_URL', default='redis://:redis_pass@redis_db:6379/1'),
    'page': ENV.cache('REDIS_URL', default='redis://:redis_pass@redis_db:6379/1'),
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "apps/schema/static"),
    os.path.join(BASE_DIR, "apps/shipments/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', default='redis://:redis_pass@redis_db:6379/1')],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Email settings
DEFAULT_FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@smtp.shipchain.io.local')
EMAIL_CONFIG = ENV.email_url('EMAIL_URL', default='smtp://:@smtp:25')
vars().update(EMAIL_CONFIG)

if ENVIRONMENT == 'INT':
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


INFLUXDB_DISABLED = True
INFLUXDB_URL = os.environ.get('INFLUXDB_URL')
if INFLUXDB_URL:
    INFLUXDB_DISABLED = False
    INFLUXDB_URL = urlparse(INFLUXDB_URL)
    INFLUXDB_HOST = INFLUXDB_URL.hostname
    INFLUXDB_PORT = str(INFLUXDB_URL.port) if INFLUXDB_URL.port else '80'
    INFLUXDB_USER = None
    INFLUXDB_PASSWORD = None
    INFLUXDB_DATABASE = INFLUXDB_URL.path[1:]
    INFLUXDB_TIMEOUT = 1

    EMAIL_BACKEND = 'influxdb_metrics.email.InfluxDbEmailBackend'

GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'
GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so'

ADMIN_PAGE_SIZE = 20
