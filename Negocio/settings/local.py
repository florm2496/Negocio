
from .base import *

DEBUG = True

ALLOWED_HOSTS = []




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'negocio',
        'HOST': '127.0.0.1',
        'PORT':'5432',
        'USER':'florm2496',
        'PASSWORD':'pan1994245',
    }
}


STATIC_URL = '/static/'

