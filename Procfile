release: python mysocial/manage.py migrate --settings mysocial.settings.production
web: gunicorn --pythonpath mysocial mysocial.wsgi