set -e

# Django
echo "Starting release"
python mysocial/manage.py migrate --settings mysocial.settings.production
echo "Database migrated"

# .keep!
touch mysocial/mysocial/staticfiles/.keep
echo "Release finished"
