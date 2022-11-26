# Remote Teams Onboarding

Hi other teams! We're team 10. Shout out to Team 14 for being the pioneers to testing our app. Here's an onboarding
document for other teams to check out!

## Setup (locally)

Follow our setup at: https://github.com/hgshah/cmput404-project/tree/staging#setup

### Deciding team 10's port

So, our server only works on two nodes: 8000 and 8080. For the tutorial, we'll use 8080.

From the get go, you have to decide which port we are running from! Like, let's say port 8080. Then, after that, don't
change it because the entries of the database is dependent on the current domain, which includes the port.

You can have another database using settings=mysocial.settings.local_mirror, but we won't cover that here.

### To create a node

### Method 0: The default ones in local testing

To make local testing easier, if your team is listed in this documentation, you might not need to set up the things
below. If your team is in here, you don't need to do the other methods below.

#### Team 14

You call our server using:
username: team14_local
password: team14_local

We call your server using:
remote_username: local_default
remote_password: local_default

This assumes that:

- team14 (your) server is running at http://127.0.0.1:8014
- team10 (our) server is running at http://127.0.0.1:8000 or http://127.0.0.1:8080

Contact us on discord if this is not feasible.

#### Team 7

You call our server using:
username: team7_local
password: team7_local

We call your server using:
remote_username: local_default
remote_password: local_default

This assumes that:

- team7 (your) server is running at http://127.0.0.1:8000
- team10 (our) server is running at http://127.0.0.1:8080

Contact us on discord if this is not feasible.

### Method 1: python manage.py shell

So... Nodes are just Authors. We sadly don't have any endpoint for that just yet!

To make a node, you might want to use the python manage.py shell:

```bash
python manage.py shell
```

```python 
from common.test_helper import TestHelper
node = TestHelper.create_node(username='team14_local', password='team14_local', remote_username='local_default', remote_password='local_default', host='127.0.0.1:8014')
node.save()
```

Note:

- Just put your dot com domain. We will handle the prefixes on our code.

### Method 2: Environment Variable

If you can add an environment variables, set `REMOTE_NODE_CREDENTIALS` to the following value:

#### Team 14

```json
{
  "127.0.0.1:8080": {
    "username": "team14_local",
    "password": "team14_local",
    "remote_username": "local_default",
    "remote_password": "local_default"
  }
}
```

Note that our server automatically detects which port it's run from and grabs the credentials in the environment
variables.

## Calling our endpoints

Call our endpoints via basic auth, and use the username and password you used to make the node!

We call your endpoint using the remote_username and remote_password fields! :D

(Yeah, I know, we don't have the POST set up yet for remote-nodes so you'll have to give us your password... T.T)

## Creating users

So, we haven't made an endpoint for making an author. The way we do it was by using the `python manage.py shell`

```python
from common.test_helper import TestHelper

node = TestHelper.create_author(username='chris')
node.save()

# new safer version that overwrites or creates a new one
node = TestHelper.overwrite_author(username='chris')
node.save()
```

The default password is "1234567".

To override properties, you can do:

```python
from common.test_helper import TestHelper

node = TestHelper.create_author(username='chris', other_args={
    'email': 'chris@gmail.com',
    'password': '1234567',
    'display_name': 'chris',
    'github': 'https://github.com/chris/',
    'is_staff': False,
    'is_superuser': False,
})
node.save()

# new safer version that overwrites or creates a new one
node = TestHelper.create_author(username='chris', other_args={
    'password': 'hunter2',
    'github': 'https://github.com/hunter2/',
    'is_staff': true,
    'is_superuser': true,
})
node.save()
```

For `other_args`, you don't need to add all fields, like the example above.

