# DO NOT DELETE THE IMPORT BELOW EVEN IF UNUSED
from mysocial.settings.local import *  # just override local
from mysocial.settings import local  # just override local
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


# for debugging purposes: figure out which setting you're on
local.LOCAL_STATE = 'MIRROR'