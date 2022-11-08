from mysocial.settings import base
from mysocial.settings.base import *
from remote_nodes.remote_util import RemoteUtil

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd2907e2jovm64i',
        'USER': 'ywprnarrdfmrak',
        'PASSWORD': 'f031d4e722ba5931280bdfcd683086d493e6de157a36d7b0eb2d1b1bf2545c50',
        'HOST': 'ec2-34-227-120-79.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# overriding production for staging configurations

# keys
DATABASE_CONFIG_KEY = "DATABASE_CONFIG"

if DATABASE_CONFIG_KEY in os.environ:
    DATABASES.update(json.loads(os.environ[DATABASE_CONFIG_KEY]))

if base.CURRENT_DOMAIN is None:
    base.CURRENT_DOMAIN = 'socioecon.herokuapp.com'

RemoteUtil.setup()
