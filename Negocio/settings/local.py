
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

APPEND_SLASH=False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'negocio2',
        'USER':'julian',
        'PASSWORD':'41060109',
        'HOST': '127.0.0.1',
        'PORT':'5432',

    }
}


STATIC_URL = '/static/'

CORS_ALLOW_ALL_ORIGINS=True
#STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
