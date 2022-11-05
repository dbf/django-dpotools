"""
Django settings for dpotools project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import sys
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fn@&36Hvrke)%e4e5)k0bf_6-$9k1^agl2jisOg_w&-gp041+z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'shibboleth',
#    'lockdown',
    'crispy_forms',
    'multiselectfield',
    'extra_views',
    'landing.apps.LandingConfig',
    'rpa.apps.RpaConfig',
    'contact.apps.ContactConfig',
#    'rosetta',
#    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'shibboleth.middleware.ShibbolethRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'lockdown.middleware.LockdownMiddleware',
]

#AUTHENTICATION_BACKENDS = (
#    'shibboleth.backends.ShibbolethRemoteUserBackend',
#    'django.contrib.auth.backends.ModelBackend',
#)
#
# The Sibboleth attribute map depends on your actual shibd config
#SHIBBOLETH_ATTRIBUTE_MAP = {
#    "cn": (True, "username"),
#    "givenName": (False, "first_name"),
#    "sn": (False, "last_name"),
#    "mail": (False, "email"),
#    "affiliation": (True, "affiliation"),
#}

ROOT_URLCONF = 'dpotools.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates/lockdown',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'dpotools.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

# Password validators are disabled to ease development and testing.  You may
# want to re-enable these in production, depending on your authenticator choice.
AUTH_PASSWORD_VALIDATORS = [
#    {
#        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#    },
#    {
#        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LOCALE_PATHS = (
    BASE_DIR / "locale",
    BASE_DIR / "dpotools/locale",
)

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
#    BASE_DIR / "rpa/static/rpa",
#    '/var/www/static/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_FAIL_SILENTLY = not DEBUG

LOGIN_URL = 'login'
#LOGIN_URL = '/Shibboleth.sso/Login'
#LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'landing:home'
LOGOUT_REDIRECT_URL = 'landing:home'

INTERNAL_IPS = [
    "127.0.0.1",
]

#LOCKDOWN_ENABLED = True

LOCKDOWN_REMOTE_ADDR_EXCEPTIONS = [
#    'YOUR_ENTITYS_IP_SUBNET',
    '127.0.0.1',
    '::1',
]

LOCKDOWN_URL_EXCEPTIONS = (
    r'^/$',
    r'^/contact/',
    r'^/i18n/',
)

#ADMINS = [
#('Erwin Lammarsch-Adler', 'erwin@some-entity.org'),
#]

#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'my_log_handler': {
#            'level': 'DEBUG' if DEBUG else 'INFO',
#            'class': 'logging.FileHandler',
#            'filename': os.path.join(BASE_DIR, 'django.log'),
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers': ['my_log_handler'],
#            'level': 'DEBUG' if DEBUG else 'INFO',
#            'propagate': True,
#        },
#    },
#}

# Rosetta
ROSETTA_POFILE_WRAP_WIDTH = 79

# Import fake local settings to provide example values,
# then overwrite with actual settings, if any.
# You may want to change this for production use.
try:
    from .local_settings_fake import *
except ImportError:
    sys.exit('Failed to import fake settings. Exiting.')

#try:
#    from .local_settings import *
#except ImportError:
#    pass
