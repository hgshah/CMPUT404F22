# Locally, our npm build is inside Socioecon1, and should not be in the root folder
# But for Heroku deployment, it's actually in the root folder so this runs differently

set -e

# Django but local
python mysocial/manage.py migrate --settings mysocial.settings.local

# Respect existing environment variables
cd Sociocon1
export SOCIOCON_TEMP_VAR=$BUILD_PATH
export BUILD_PATH="../mysocial/mysocial/staticfiles/"
npm install
npm run build
export BUILD_PATH=$SOCIOCON_TEMP_VAR
cd ..

# .keep!
touch mysocial/mysocial/staticfiles/.keep
touch mysocial/mysocial/staticfiles/static/loadbearing_file.txt
python mysocial/manage.py runserver # might run into issue inside python env
