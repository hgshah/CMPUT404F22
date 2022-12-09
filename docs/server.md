# Server

Note: Most of the documentation here are based on @TurnipXenon's experience.

## Setting up a Heroku app (server instance)

1. Fork the repository. Heroku only works on main or master branch, sadly.
   ```
   # How to add a staging branch locally (exampple)
   git remote add amanda-staging git@github.com:CMPUT301W20T10/amanda-staging.git
   git fetch amanda-staging
   git checkout -b amanda-staging amanda-staging/main
   git pull origin staging # or main
   git push amanda-staging main
   ```
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

### Code Changes

To add another node instance, and let our code handle logic for it differently. We a NodeConfig class for it. To do
that:

1. Create a class that inherits **NodeConfigBase**. See `remote_nodes/potato_oomfie.py` as a basic reference
    - The extent that we override functions or values is up to how different our Node is (not relevant for Team 10 lol)

```python
from remote_nodes.node_config_base import NodeConfigBase


class PotatoOomfie(NodeConfigBase):
    domain = 'potato-oomfie.herokuapp.com'  # update based on your domain!
```

2. Register this class in **RemoteUtil.py**

```python
class RemoteUtil:

    @staticmethod
    def setup():
        """Register your NodeConfig class over here"""
        for config in (TurnipOomfie, PotatoOomfie):  # add you class here!!!
            base.REMOTE_CONFIG.update(config.create_dictionary_entry())
```

## Workflow

**What's the difference between staging and production?**

When pushing to staging, you deploy two mirror servers. It helps you test out before pushing to production.

When pushing to production, it only deploys to Socioecon. Make sure nothing breaks when you do this.

### Pushing to staging

The workflow for deploying to staging is:

1. Make sure you have the git origin url to staging. If not,
   do `git add remote staging1 git@github.com:TurnipXenon/cmput404-project-personal-staging.git`
2. Work on a branch based on staging, let's call this *current-branch*.
3. If you want to test your changes locally, you can
   run `python manage.py runserver --settings mysocial.settings.production`.
4. If you want to push your changes to heroku, you push your changes to staging by running the git
   command `git push staging current-branch:main`. (like `git push staging1 staging1:main`)
    - This follows the format: `git push origin diff-branch:main` which pushes your local `diff-branch` to the
      branch `main` at the remote repository `origin`.
    - If this is confusing and prone to errors, you may just push your differently-named branch to your fork's
      repository and do a pull request that merges to main.
    - If you're manually deploying, like the instruction in the setup, go to your app's Deploy tab and manually deploy.
    - You can use the same branch to push to our main repo like `git push origin current-branch`.

### Pushing to production

1. Make sure you have the git origin url to production. If not,
   do `git remote add production https://git.heroku.com/socioecon.git`
2. If you want to push your changes to heroku, you push your changes to production by running the git
   command `git push production current-branch:master`.

Reference:
```bash
git remote add production https://git.heroku.com/socioecon.git
git checkout staging
git pull origin staging
git push production staging:master
```

## Adding another team to our server

As a case study, we're gonna pretend that we're adding Team14 to our server.

#### Part 1: Create NodeConfigBase override for them!

We created `remote_nodes/team14_local.py` for local testing, and `remote_nodes/team14_main.py` for production. The
structure looks like this:

**team14_local.py**

```python
import json

import requests

from common.base_util import BaseUtil
from remote_nodes.local_default import LocalDefault


class Team14Local(LocalDefault):
    domain = '127.0.0.1:8014'  # domain/host of their url extracted using `from urllib.parse import urlparse`
    username = 'team14'  # username they will use to call us

    # you can override the field mappings, look at remote_fields

    def get_base_url(self):
        """
        You can override the base url like this!
        Use self.__class__.domain so we also get changes from child classes and not this one.
        Look at Team14Main which inherites Team14Local
        """
        return f'{BaseUtil.get_http_or_https()}{self.__class__.domain}/api'

    @classmethod
    def create_node_credentials(cls):
        """This is for local testing"""
        return {
            cls.domain: {
                'username': 'team14_local',
                'password': 'team14_local',
                'remote_username': 'local_default',
                'remote_password': 'local_default',
            }
        }

    # feel free to override other methods!
```

**team14_main.py**

```python
from remote_nodes.team14_local import Team14Local


class Team14Main(LocalDefault):
    domain = 'team14.herokuapp.com'  # domain/host of their url extracted using `from urllib.parse import urlparse`
    username = 'team14'  # username they will use to call us

    # you can override the field mappings, look at remote_fields

    # feel free to override other methods!
```

### Part 2: RemoteUtil

Add the classes above to RemoteUtil's
connected_node_classes [in these lines](https://github.com/hgshah/cmput404-project/blob/03111274817d6978d0b81e41b61a98839e92c5b7/mysocial/remote_nodes/remote_util.py#L59-L62)

```python
from remote_nodes.team14_local import Team14Local
from remote_nodes.team14_main import Team14Main

# ...

if '127.0.0.1' in base.CURRENT_DOMAIN:
    connected_node_classes = [LocalDefault, LocalMirror, Team14Local]
else:
    connected_node_classes = [TurnipOomfie, PotatoOomfie, UAlberta, MacEwan, Team14Main, Socioecon]
```

### Part 3: ConfigVars

In socioecon's ConfigVars (or staging), add this with key REMOTE_NODE_CREDENTIALS:

*This ConfigVars assumes that it's in socioecon*

```json
{
  "potato-oomfie.herokuapp.com": {
    "username": "potato",
    "password": "potato's password when calling socioecon",
    "remote_username": "socioecon",
    "remote_password": "socioecon's password when calling potato"
  },
  "team14.herokuapp.com": {
    "username": "team14",
    "password": "team14's password when calling socioecon",
    "remote_username": "team10",
    "remote_password": "socioecon's password when calling team14"
  }
}
```

### Part 4: Double deploy... (Some funky issues I haven't solved)

We have a weird bug where you might need to deploy twice due to some ordering with node creation and node config
creation. Might not solve this bug, but we could just deploy twice once we add a new REMOTE_NODE_CREDENTIALS. You may do
this by adding a comment anywhere, then pushing it again.
