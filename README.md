# CMPUT404F22

hgshah
amanda6
hsmalhi
manuba
junhong1

## Setup

Before you start:
Start your virtual env!
pip install -r requirements.txt

## Running locally

Due to the project's structure, we only support running this server in two ports: `8000` (default) and `8080`

To run locally in the `8000` port:

```bash
python manage.py runserver
# If things don't work, try
python manage.py runserver --settings mysocial.settings.local
```

Note: I tested this out. I find it weird how it works without the mysocial.settings.local key in bash for windows (which
behaves more closely to Unix) but does not work in windows powershell (running Pycharm django runserver). If omitting
the settings key causes an error, try adding it.

To run locally in the `8080` port:

```bash
python manage.py runserver 8080
# If things don't work, try...
python manage.py runserver --settings mysocial.settings.local 8080
```

**Note**: the **port** argument should always be last.

## Switching to PostgresDB (MACOS)
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

Windows Instruction:

1. pip install -r requirements.txt

2. Download postgres through here https://www.enterprisedb.com/downloads/postgres-postgresql-downloads password = password, port = 5432

3. Add the postgres path here: https://blog.sqlbackupandftp.com/setting-windows-path-for-postgres-tools

4. Re-open a new command prompt so the path variables can reset

5. Go into cmput404-project/mysocial

6. psql postgres, password: password

7. CREATE DATABASE mysocialdb;

8. \connect mysocialdb

9. CREATE ROLE mysocialuser WITH LOGIN PASSWORD 'password';

10. ALTER ROLE mysocialuser CREATEDB;

11. CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO mysocialuser; GRANT ALL ON SCHEMA public TO public;

12. \q to exit out of psql

Continue from step 8

## Mirror instance

This is a setup on how to run another Django server in a different port

### Postgres

These instructions are in Windows! Inside `psql`:

1. `CREATE DATABASE mysocialdb_mirror;`
2. `\connect mysocialdb_mirror`
3. `ALTER ROLE mysocialuser CREATEDB;`
   - Note: if you followed the initial step of making a database, you should have mysocialuser already
4. `GRANT ALL ON SCHEMA public TO mysocialuser; GRANT ALL ON SCHEMA public TO public;`
   - Schema public already exists!

### Migration

Migration is slightly different!

```bash
python manage.py migrate --settings mysocial.settings.local_mirror
```

### Running your mirror server

Then, to run your mirror server:

```bash
python manage.py runserver --settings mysocial.settings.local_mirror 8080
```

Note:
- The port 8080 matters because that's the node we want to connect to based on NODE_CREDENTIALS. See RemoteUtils.py.
- The port number being the last argument matters, though!

You must run the postgres database as you're running the server!