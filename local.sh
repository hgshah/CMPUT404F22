# Django but local
python mysocial/manage.py migrate --settings mysocial.settings.local

# Respect existing environment variables
export SOCIOCON_TEMP_VAR=$BUILD_PATH
export BUILD_PATH="../mysocial/mysocial/staticfiles/"
npm run --prefix Sociocon1 build
export BUILD_PATH=$SOCIOCON_TEMP_VAR

# .keep!
touch mysocial/mysocial/staticfiles/.keep

python mysocial/manage.py runserver
