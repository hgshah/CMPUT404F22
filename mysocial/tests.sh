# To run, `bash tests.sh`

for p in "authors" "comment" "common" "follow" "post" "tokens"; do
  # from https://unix.stackexchange.com/a/589382
  python manage.py test $p || break
done
