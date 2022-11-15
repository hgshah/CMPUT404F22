from mysocial.settings.base import *
from mysocial.settings import base

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mysocialdb',
        'USER': 'mysocialuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

if base.CURRENT_DOMAIN is None:
    base.CURRENT_DOMAIN = f'127.0.0.1:{base.CURRENT_PORT}'
