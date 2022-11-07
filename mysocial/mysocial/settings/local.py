from mysocial.settings.base import *

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
