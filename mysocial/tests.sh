# To run, `bash tests.sh`

for p in "comment" "post"; do
  # from https://unix.stackexchange.com/a/589382
  python manage.py test $p --settings mysocial.settings.local || break
done
