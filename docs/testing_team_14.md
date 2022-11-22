# Testing Team 14

This guide is for local setup.

## Setup

Follow their setup: https://github.com/zarifmahfuz/project-socialdistribution#setup

When running their server, run it on port 8014:

```bash
python manage.py runserver 8014
```

## Creating a node on their server

Call POST on `127.0.0.1:8014/api/nodes` with this payload:
```json
{
  "api_url": "http://127.0.0.1:8014",
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
