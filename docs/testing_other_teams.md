# Testing Other Teams

This guide is for local setup.

## Team 14

### Setup

Follow their setup: https://github.com/zarifmahfuz/project-socialdistribution#setup

When running their server, run it on port 8014:

```bash
python manage.py runserver 8014
```

### Creating a node on their server

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

## Team 7

### Setup

1. First, you gotta install MongoDB: https://www.mongodb.com/try/download/community. Just choose all the default
   options!
2. Follow their setup: https://github.com/irriss-nn/group-cmput404-project#setup-virtual-environment
3. Change the port to 9007 in main.py.
   From:
   ```python
   if __name__ == "__main__":
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)
   ```
   To:
   ```python
   if __name__ == "__main__":
        uvicorn.run("main:app", host="localhost", port=8007, reload=True)
   ```
   To test on our end, run the server in port 8007.
4. Run server with `python main.py`

### Sanity check

Our headers and auth maybe wrong, so to sanity check that the basics are correct.

To test their local server:

```curl
curl -u team7_local:team7_local -H 'Origin: http://127.0.0.1:8000' http://127.0.0.1:8007
```

To test their production server:

```curl
curl -u team10:pot8os_are_tasty -H 'Origin: https://socioecon.herokuapp.com' https://cmput404-social.herokuapp.com/remote-node
```

## Team 12

### Setup

1. Follow their guide: https://github.com/bconklinua/404-group#404-group
2. `python manage.py migrate`
3. Run the server at port 8012: `python manage.py runserver 8012` just to make sure it runs. Check
   out `http://127.0.0.1:8012/login`
4. Create an account using `python manage.py createsuperuser` with the following credentials
    - email: team10_local@mail.com
    - username: team10_local
    - password: team10_local

### Sanity check

To test their local server, first, we try to obtain a token:

```curl
curl --location --request POST 'http://127.0.0.1:8012/api/auth/token/obtain/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "team10@mail.com",
    "password": "team10_local"
}'
```

The response should look like:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NzMwNTIzOCwiaWF0IjoxNjcwMDI1MjM4LCJqdGkiOiI4MmYyMDYzMTJlYWE0MGNhYTdhMTlkZjBkMmEwY2FhMSIsInVzZXJfZW1haWwiOiJ0ZWFtMTBAbWFpbC5jb20ifQ.lLA2yrQP1NRElS8NeCO0g20Y8PBM7PIXgBCEhh2XPFk",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4NjY1MjM4LCJpYXQiOjE2NzAwMjUyMzgsImp0aSI6IjgzMjJlNzBkYzc5ZjQ2M2I5MTliNWM1ODc4MDRmMmUwIiwidXNlcl9lbWFpbCI6InRlYW0xMEBtYWlsLmNvbSJ9.w_oGofHb1e-XkBKz0GwMgQPiuRmWosTMJ1Q91S8SX6A"
}
```

Take the access field from the curl request you did and put it in the header. To test their auth endpoints:

```curl
curl --location --request GET 'http://127.0.0.1:8012/api/auth/test/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4NjY1NDQwLCJpYXQiOjE2NzAwMjU0NDAsImp0aSI6ImY2MWJiNjhkZTRkYzRiOGI4N2U2YjI4ZTI4OWYxYjAwIiwidXNlcl9lbWFpbCI6InRlYW0xMEBtYWlsLmNvbSJ9.mqXSlOlsle8oJxS3UpnjnB4Pws_YrfgKvvyTbdcW_Kg'
```

The response should look like:

```
authenticated
```

