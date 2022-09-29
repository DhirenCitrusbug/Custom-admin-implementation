"""
Django settings for reeach_will project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from email.policy import default
import os
from re import L

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
from os import path
from pathlib import Path
import environ
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, path.join(BASE_DIR, 'admin'))
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR / ".env"))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i1os8g&bns#wcm-==q9nyc998pmp$3n+y32p%e@73dmhotvh+s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_user',
    'aegency_user',
    'client',
    'client_user',
    'crispy_forms',
    'customadmin'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'reeach_will.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'reeach_will.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'admin_user.Admin'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = path.join(BASE_DIR, 'media').replace('\\', '/')

MEDIA_URL = '/media/'


STATIC_ROOT = path.join(BASE_DIR, 'static').replace('\\', '/')



STATICFILES_DIRS = (
    path.join(BASE_DIR, 'reaach_will', 'static'),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
LOCAL_EMAIL=env('LOCAL_EMAIL', default='')
COUPON_URL=env('COUPON_URL', default='')
PHONE_WEBHOOK=env('PHONE_WEBHOOK', default='')



SESSION_COOKIE_AGE = 60 * 60 * 24 * 30


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'



SENDGRID_API_KEY =  env("SENDGRID_API_KEY")
FROM_EMAIL=env('FROM_EMAIL', default='')
INACTIVE_USER_TEMPLATE=env('INACTIVE_USER_TEMPLATE', default='')
ACTIVE_USER_TEMPLATE=env('ACTIVE_USER_TEMPLATE', default='')
WELCOME_TEMPLATE=env('WELCOME_TEMPLATE', default='')
FORGOT_TEMPLATE=env('FORGOT_TEMPLATE', default='')
CLIENT_USER_WELCOME_TEMPLATE=env('CLIENT_USER_WELCOME_TEMPLATE', default='')
AGENCY_WELCOME_TEMPLATE=env('AGENCY_WELCOME_TEMPLATE', default='')
AGENCY_ACTIVE_USER_TEMPLATE=env('AGENCY_ACTIVE_USER_TEMPLATE', default='')
AGENCY_INACTIVE_USER_TEMPLATE=env('AGENCY_INACTIVE_USER_TEMPLATE', default='')
CLIENT_USER_ACTIVE_TEMPALATE=env('CLIENT_USER_ACTIVE_TEMPALATE', default='')
CLIENT_USER_INACTIVE_TEMPALATE=env('CLIENT_USER_INACTIVE_TEMPALATE', default='')


WELCOME_AGENCY_SUBJECT=env("WELCOME_AGENCY_SUBJECT")
WELCOME_CLIENT_SUBJECT=env("WELCOME_CLIENT_SUBJECT")
AGENCY_ACTIVE_SUBJECT=env("AGENCY_ACTIVE_SUBJECT")
AGENCY_INACTIVE_SUBJECT=env("AGENCY_INACTIVE_SUBJECT")
CLIENT_ACTIVE_SUBJECT=env("CLIENT_ACTIVE_SUBJECT")
CLIENT_INACTIVE_SUBJECT=env("CLIENT_INACTIVE_SUBJECT")
CLIENT_USER_ACTIVE_SUBJECT=env("CLIENT_USER_ACTIVE_SUBJECT")
CLIENT_USER_INACTIVE_SUBJECT=env("CLIENT_USER_INACTIVE_SUBJECT")
AGENCY_FORGOT_PASSWORD=env("AGENCY_FORGOT_PASSWORD")
CLIENT_FORGOT_PASSWORD=env("CLIENT_FORGOT_PASSWORD")
CLIENT_USER_PASSCODE=env("CLIENT_USER_PASSCODE")

# Referral Campaign

REFERRAL_CAMPAIGN_URL=env('REFERRAL_CAMPAIGN_URL', default='')

# Cloudflare Account Details

CLOUDFLARE_ACCOUNT_EMAIL=env('CLOUDFLARE_ACCOUNT_EMAIL', default='')
CLOUDFLARE_ACCOUNT_TOKEN=env('CLOUDFLARE_ACCOUNT_TOKEN', default='')
CLOUDFLARE_ACCOUNT_ID=env('CLOUDFLARE_ACCOUNT_ID', default='')
CLOUDFLARE_ZONE_ID=env('CLOUDFLARE_ZONE_ID', default='')
CLOUDFLARE_API_URL=env('CLOUDFLARE_API_URL', default='')

LOGIN_REDIRECT_URL = '/customadmin'
LOGOUT_REDIRECT_URL = '/customadmin/login'