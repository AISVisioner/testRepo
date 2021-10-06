from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     'postgres',
        'USER':     'postgres',
        'PASSWORD': 'postgres',
        'HOST':     'db',
        'PORT':     '5432',
    }
}