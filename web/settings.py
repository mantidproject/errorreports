"""
Django settings for docker_django project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'NO').lower() in ('on', 'true', 'y', 'yes')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = '/usr/src/app/recovery'
MEDIA_URL = '/api/download/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'django_filters',
    'markdown',
    'rest_framework',
    'services',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'

REST_FRAMEWORK = {
    'FORM_METHOD_OVERRIDE': None,
    'FORM_CONTENT_OVERRIDE': None,
    'FORM_CONTENTTYPE_OVERRIDE': None
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )
# print(STATICFILES_DIRS)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Logging
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
            'slack': {
                'level': 'ERROR',
                'class': 'handlers.SlackHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'slack'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            },


        },
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'logfile': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/django.log',
                'maxBytes': 1024*1024*15,  # 15MB
                'backupCount': 10,
            },
            'slack': {
                'level': 'ERROR',
                'class': 'handlers.SlackHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['logfile', 'slack'],
                'level': 'ERROR',
            },

        },
    }


# Slack notifications can be configured by environment variables
# webhook is required, everything else is optional
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', None)
SLACK_ERROR_REPORTS_CHANNEL = os.getenv('SLACK_ERROR_REPORTS_CHANNEL',
                                        '#error-reports')
SLACK_SERVER_ERRORS_CHANNEL = os.getenv('SLACK_SERVER_ERRORS_CHANNEL',
                                        '#linode-app-errors')
SLACK_ERROR_REPORTS_USERNAME = os.getenv('SLACK_ERROR_REPORTS_USERNAME',
                                         'Error Reporter')
SLACK_ERROR_REPORTS_EMOJI = os.getenv('SLACK_ERROR_REPORTS_EMOJI',
                                      ':sadmantid:')
SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT = os.getenv(
    'SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT', 'Not provided')


# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
