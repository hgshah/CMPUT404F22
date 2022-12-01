# Django
python mysocial/manage.py migrate --settings mysocial.settings.production

# Respect existing environment variables
export SOCIOCON_TEMP_VAR=$BUILD_PATH
export BUILD_PATH="../mysocial/mysocial/staticfiles/"
npm run build Sociocon1
export BUILD_PATH=$SOCIOCON_TEMP_VAR

# .keep!
touch mysocial/mysocial/staticfiles/.keep
