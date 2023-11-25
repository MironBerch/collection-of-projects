from os import environ
from pathlib import Path
from socket import gethostbyname_ex, gethostname

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get('ADMIN_SECRET_KEY')

DEBUG = int(environ.get('DEBUG'))

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # drf
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',

    # django 3rd party
    'django_filters',
    'debug_toolbar',

    # local
    'api.apps.ApiConfig',
    'movies.apps.MoviesConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('ADMIN_POSTGRES_DB'),
        'USER': environ.get('ADMIN_POSTGRES_USER'),
        'PASSWORD': environ.get('ADMIN_POSTGRES_PASSWORD'),
        'HOST': environ.get('ADMIN_POSTGRES_HOST'),
        'PORT': environ.get('ADMIN_POSTGRES_PORT'),
    },
}


# Password validation

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


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# INTERNAL IPS configuration

hostname, _, ips = gethostbyname_ex(gethostname())
INTERNAL_IPS = [ip[: ip.rfind('.')] + '.1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

# REST_FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'MOVIES API',
    'VERSION': None,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]+/',
    'SCHEMA_PATH_PREFIX_TRIM': True,
    'SERVE_AUTHENTICATION': ['rest_framework.authentication.SessionAuthentication'],
    'SERVE_PERMISSIONS': ['api.permissions.IsSuperUser'],
}
