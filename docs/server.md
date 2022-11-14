# Server

Note: Most of the documentation here are based on @TurnipXenon's experience.

## Setting up a Heroku app (server instance)

1. Fork the repository. Heroku only works on main or master branch, sadly.
2. Create a Heroku app.
3. Under the Resources tab, create a Postgres add-on.
4. Go to your Postgres add-on's setting, and click **View Credentials** to see your **Database Credentials**
5. In your app's Settings tab, under the Config Vars' section. Add the following key-value pair Config Vars:
    1. CURRENT_DOMAIN (required): your app's domain
    2. DATABASE_CONFIG (required unless it's local or the production instance): a STRICT json file of database config to
       override the current production one
    3. DATABASE_URL (required; auto-generated): URL to the Postgres Resource you made in Step 3
    4. DJANGO_SETTINGS_MODULE (required): mysocial.settings.production
    5. REMOTE_NODE_CREDENTIALS (required): A dictionary of username-password credentials for a particular domain. This
       makes remote node type Author objects for you, and activates them.
    6. PREFILLED_USERS (optional): A dictionary containing the field items, which is a list of Authors we want to
       pre-populate our server with. Useful for having an initial superuser or not having to need to make Authors again
       every time you wipe your database

    - Tip for making JSON files: JSON structures can be a little strict leading to parsing errors. Make an empty JSON
      file, and edit them in your IDE. Install plugins that prettifies or lints JSON files
    - This is what the Config Vars potato-oomfie.herokuapp.com looks like this:

```
CURRENT_DOMAIN: potato-oomfie.herokuapp.com

# notes:
# - do NOT add a comma at the last entry of default, right after PORT: 5432
# - change the entries based on the credentials you saw in step 4
# - the only entry you shouldn't change below is ENGINE and PORT
DATABASE_CONFIG: {
   "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "DATABASE NAME (Database Field)",
        "USER": "DATABASE USER",
        "PASSWORD": "DATABASE PASSWORD",
        "HOST": "ec2-54-163-34-107.compute-1.amazonaws.com",
        "PORT": "5432"
   }
}

DATABASE_URL: postgres://url

DJANGO_SETTINGS_MODULE: mysocial.settings.production

# A dictionary of domain-credential pairs
# Credentials follow the following pattern:
# "domain_url": {
#   "username": string,
#   "password": string,
#   "is_active": bool
# } 
# Implicitly creates and activates a node-type Author for node-to-node communication
# You can explcitly activate a node by saying is_active = True
# You can explcitly disable a node by saying is_active = False
# If a node was previously inactive and the is_active field was missing, it will be activated
REMOTE_NODE_CREDENTIALS: {
  "127.0.0.1:8000": {
    "username": "local",
    "password": "password"
  },
  "potato-oomfie.herokuapp.com": {
    "username": "potato",
    "password": "password",
    "is_active": True
  },
  "turnip-oomfie-1.herokuapp.com": {
    "username": "turnip",
    "password": "password",
    "is_active": False
  }
}

# A list of Authors following the pattern:
# {
#   "items": [
#    {
#       "username": string/required,
#       "password": string/required,
#       "is_staff": bool/optional, <- if you need admin
#       "is_superuser": bool/optional, <- if you need admin
#    }
# ]
# }
PREFILLED_USERS: {
  "items": [
    {
      "username": "super",
      "password": "super",
      "is_staff": true,
      "is_superuser: true
    },
    {
      "username": "actor",
      "password": "actor"
    },
    {
      "username": "target",
      "password": "target"
    }
  ]
}
```

6. Under your app's Deploy tab, connect to Github (or manually push via heroku's cli)
7. It would be nice to auto-deploy to so Enable Automatic Deploy if you like
    - Note: if you have multiple apps connected to the same Github repo, both will fail deploying since the free tier
      can only support one build at a time.
8. Either push to your main or manually deploy your branch under the Deploy tab in your app.
9. Remember to create a superuser!
    - This is another way of making a user! Or you can use the PREFILLED_USERS ConfigVar in Step 5.
    - In the heroku CLI, you can
      do `heroku run python mysocial/manage.py createsuperuser --settings mysocial.settings.production --app app-name`
    - In the heroku web GUI
        1. At the top-right **More**, click it.
        2. It will show a drop-down menu. Choose `Run console`.
        3. In the dialog box that showed up,
           enter: `python mysocial/manage.py createsuperuser --settings mysocial.settings.production`
10. For my workflow, I've added my remote fork repository
    with `git add remote new-remote-origin-nickname git@github.com/user/fork-repo.git`
11. Since we have similar named mains for different remote origins, you have to checkout to your remote fork origin's
    main, like this `git checkout -b my-main new-remote-origin-nickname/main`. Doing your standard `git checkout main`
    would default to `origin/main` in our main repository.
12. You can set up another app by repeating steps 2 to 11 if I want remote servers set up with duplicated codes but
    different configs. Note that automatic deployment will fail if more than one Django is being built in one Heroku
    account.

## Workflow

1. Work on a branch based on staging, let's call this *current-branch*.
2. If I want to test my changes locally, I can run `python manage.py runserver --settings mysocial.settings.production`.
3. If I want to test my changes in heroku, I push my changes to my personal main fork by running the git.
   command `git push your-fork-origin current-branch:main`.
    - This follows the format: `git push origin diff-branch:main` which pushes your local `diff-branch` to the
      branch `main` at the remote repository `origin`.
    - If this is confusing and prone to errors, you may just push your differently-named branch to your fork's
      repository and do a pull request that merges to main.
    - If you're manually deploying, like the instruction in the setup, go to your app's Deploy tab and manually deploy.
    - I can use the same branch to push to our main repo like `git push origin current-branch`.
