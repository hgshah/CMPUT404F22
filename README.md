# CMPUT404F22
hgshah
amanda6
hsmalhi
manuba
junhong1

Before you start:
Start your virtual env!
pip install -r requirements.txt

Switching to PostgresDB (MACOS)
https://daily-dev-tips.com/posts/installing-postgresql-on-a-mac-with-homebrew/
Installing postgres

1. brew update

2. brew install postgresql

To start the database:
3. brew services start postgresql

4. psql postgres

5. CREATE DATABASE mysocialdb;

6. CREATE ROLE mysocialuser WITH LOGIN PASSWORD 'password';

7. ALTER ROLE mysocialuser CREATEDB;

exit out of psql (command + z)

8. python manage.py makemigrations

9. python manage.py migrate

10. python manage.py createsuperuser

To start the database:
brew services start postgresql

To stop the database:
brew services stop postgresql

You must run the postgres database as you're running the server!

Windows Instruction:

1. pip install -r requirements.txt

2. Download postgres through here https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
password = password, port = 5432

3. Add the postgres path here: https://blog.sqlbackupandftp.com/setting-windows-path-for-postgres-tools

4. Re-open a new command prompt so the path variables can reset

5. Go into cmput404-project/mysocial

6. psql postgres, password: password

7. CREATE DATABASE mysocialdb;

8. \connect mysocialdb

9. CREATE ROLE mysocialuser WITH LOGIN PASSWORD 'password';

10. ALTER ROLE mysocialuser CREATEDB;

11.
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO mysocialuser;
GRANT ALL ON SCHEMA public TO public;

12. \q to exit out of psql

13. Continue from step 8

To Run the Server 
python manage.py migrate --settings mysocial.settings.local
python manage.py runserver --settings mysocial.settings.local

References:
Amanda
https://stackoverflow.com/questions/5255913/kwargs-in-django
https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
https://stackoverflow.com/questions/31173324/django-rest-framework-update-field
https://stackoverflow.com/questions/43859053/django-rest-framework-assertionerror-fix-your-url-conf-or-set-the-lookup-fi
https://stackoverflow.com/questions/62381855/how-to-update-model-objects-only-one-field-data-when-doing-serializer-save
https://stackoverflow.com/questions/35024781/create-or-update-with-put-in-django-rest-framework
https://stackoverflow.com/questions/1496346/passing-a-list-of-kwargs
https://stackoverflow.com/questions/70878647/login-to-django-admin-via-requests
https://www.youtube.com/watch?v=1FqxfnlQPi8&ab_channel=pymike00
https://stackoverflow.com/questions/44604686/how-to-test-a-model-that-has-a-foreign-key-in-django
https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
https://stackoverflow.com/questions/16416172/how-can-i-modify-procfile-to-run-gunicorn-process-in-a-non-standard-folder-on-he
https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django
https://www.youtube.com/watch?v=5d8AQFF0Ot0&t=689s&ab_channel=CodeAura
https://www.linkedin.com/pulse/migrating-my-django-app-database-postgresql-onheroku-jovanta-pelawi/
https://stackoverflow.com/questions/68265591/why-it-shows-unknown-command-collectstatic-when-i-try-to-collect-static
https://stackoverflow.com/questions/15128135/setting-debug-false-causes-500-error#:~:text=If%20you%20are%20having%20a,in%20any%20web%20error%20logs.