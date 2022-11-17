# Remote Teams Onboarding

Hi other teams! Shout out to Team 14 for being the pioneers to testing our app. Here's an onboarding document for other
teams to check out!

## Setup

Follow our setup at: https://github.com/hgshah/cmput404-project/tree/staging#setup

## To create a node

### Method 1: python manage.py shell

So... Nodes are just Authors. We sadly don't have any endpoint for that just yet!

To make a node, you might want to use the python manage.py shell:

```bash
python manage.py shell
```

```python 
from common.test_helper import TestHelper
node = TestHelper.create_node(username='team-oomf', password='hunter2', remote_username='team-oomf', remote_password='hunter3', host='www.team-oomf.herokuapp.com')
node.save()
```

Note:

- Just put your dot com domain. We will handle the prefixes on our code.

### Method 2: Enviroment Variable

If you can add an environment variables, set `REMOTE_NODE_CREDENTIALS` to the following value:

```json
{
  "127.0.0.1:8000": {
    "username": "team-oomf",
    "password": "hunter2",
    "remote_username": "team-oomf",
    "remote_password": "hunter3"
  }
}
```

## Calling our endpoints

Call our endpoints via basic auth, and use the username and password you used to make the node!
