# Testing Team 14

This guide is for local setup.

## Setup

Follow their setup: https://github.com/zarifmahfuz/project-socialdistribution#setup

When running their server, run it on port 8014:

```bash
python manage.py runserver 8014
```

## Creating a node on their server

![img.png](img.png)

Also we kinda need to comment out this lines to override auth. Quick way to do the call below

Call POST on `127.0.0.1:8014/api/nodes` with this payload:
```json
{
  "api_url": "http://127.0.0.1:8000/",
  "node_name": "local_default",
  "password": "local_default",
  "password2": "local_default",
  "auth_username": "team14_local",
  "auth_password": "team14_local",
  "team": 10
}
```

We call their endpoint with auth_username and auth_password.

They call our endpoint with node_name and password.

As a sanity check, try to connect to their endpoint as a node.

![img_1.png](img_1.png)
