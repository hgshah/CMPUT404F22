# Django
echo "Starting release"
python mysocial/manage.py migrate --settings mysocial.settings.production
echo "Database migrated"

# Respect existing environment variables
export SOCIOCON_TEMP_VAR=$BUILD_PATH
export BUILD_PATH="../mysocial/mysocial/staticfiles/"
npm run build Sociocon1
echo "React app built"
export BUILD_PATH=$SOCIOCON_TEMP_VAR

# .keep!
touch mysocial/mysocial/staticfiles/.keep
echo "Release finished"
