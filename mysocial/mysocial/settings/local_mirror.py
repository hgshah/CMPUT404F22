# DO NOT DELETE THE IMPORT BELOW EVEN IF UNUSED
from mysocial.settings.local import *  # just override local
# DO NOT DELETE THE IMPORT ABOVE EVEN IF UNUSED

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mysocialdb_mirror',
        'USER': 'mysocialuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
