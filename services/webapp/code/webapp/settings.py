"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured
from webapp.core.utils import booleanize

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '-3byo^nd6-x82fuj*#68mj=5#qp*gagg58sc($u$r-=g8ujxu4')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = booleanize(os.environ.get('DJANGO_DEBUG', False))

# SECURITY WARNING: check if you want this in production
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'webapp.core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

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

WSGI_APPLICATION = 'webapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

default_db_engine = 'django.db.backends.sqlite3'
default_db_name   = os.path.join(BASE_DIR, '../webapp_database.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE', default_db_engine),
        'NAME': os.environ.get('DJANGO_DB_NAME', default_db_name),
        'USER': os.environ.get('DJANGO_DB_USER', None),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', None),
        'HOST': os.environ.get('DJANGO_DB_HOST', None),
        'PORT': os.environ.get('DJANGO_DB_PORT',None),
    }
}




# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'         # URL path
STATIC_ROOT = '/webapp/static'  # Filesystem path


# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100000
}

# Swagger settings
# See https://django-rest-swagger.readthedocs.io/en/latest/settings/

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {},
    'USE_SESSION_AUTH': False
}

# Public host
PUBLIC_HOST = os.environ.get('PUBLIC_HOST', 'localhost')

#===============================
#  Email settings
#===============================

DJANGO_EMAIL_SERVICE = os.environ.get('DJANGO_EMAIL_SERVICE', 'Sendgrid')
if not DJANGO_EMAIL_SERVICE in ['Sendgrid', None]:
    raise ImproperlyConfigured('Invalid EMAIL_METHOD ("{}")'.format(DJANGO_EMAIL_SERVICE))
DJANGO_EMAIL_FROM = os.environ.get('DJANGO_EMAIL_FROM', 'Web App <notifications@web.app')
DJANGO_EMAIL_APIKEY = os.environ.get('DJANGO_EMAIL_APIKEY', None)


#===============================
#  Logging
#===============================

DJANGO_LOG_LEVEL  = os.environ.get('DJANGO_LOG_LEVEL','ERROR')
WEBAPP_LOG_LEVEL = os.environ.get('WEBAPP_LOG_LEVEL','ERROR')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
 
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s',
        },
        'halfverbose': {
            'format': '%(asctime)s, %(name)s: [%(levelname)s] - %(message)s',
            'datefmt': '%m/%d/%Y %I:%M:%S %p'
        }
    },
 
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
 
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'halfverbose',
        },
    },
 
    'loggers': {
        'webapp': {
            'handlers': ['console'],
            'level': WEBAPP_LOG_LEVEL,
            'propagate': False, # Do not propagate or the root logger will emit as well, and even at lower levels. 
        },
        'django': {
            'handlers': ['console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': False, # Do not propagate or the root logger will emit as well, and even at lower levels. 
        }, 
        # Read more about the 'django' logger: https://docs.djangoproject.com/en/2.2/topics/logging/#django-logger
        # Read more about logging in the right way: https://lincolnloop.com/blog/django-logging-right-way/
    }
}
