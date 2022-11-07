# Remote Node

Remote nodes are just normal users with a special hidden type. It can be activated and reactivated by the server admin.

## How to add a remote node in the server

1. Create a user in your commandline via `shell`

- For heroku deploys, use `heroku run python manage.py shell [-a app-name]`
- For local servers, use `python manage.py shell`
  Within the shell, enter the following:

```python
from common.test_helper import TestHelper

node = TestHelper.create_node(username='team-oomf', password='hunter2', host='www.team-oomf.herokuapp.com')
node.save()
exit()
```

- Note: For host in this step: use the remote host! (OR your host if you want to connect with us)
- Note: you cannot make this in `admin/`, because the password is encrypted!

2. In `admin/`, make sure that the **Author type**: is **Active Remote Node**
3. Test out Basic Auth by calling our endpoint (user OUR host not yours aka not the remote):

```shell
# curl local
curl http://team-oomf:hunter2@127.0.0.1:8000/remote-node/

# curl remote
# todo(turnip): change when we have actual domain
curl http://team-oomf:hunter2@www.sociocon.herokuapp.com/remote-node/

# alternatively: httpie
http -a team-oomf:hunter2 http://www.sociocon.herokuapp.com/remote-node/
````

If you want to try it in your browser, **logout from your admin or clear current cookies or local storage,**
and then click this link:
[http://team-oomf:hunter2@127.0.0.1:8000/remote-node/](http://team-oomf:hunter2@127.0.0.1:8000/remote-node/)

The result should look like:

```json
{
  "message": "Authentication passed!",
  "type": "remoteNode"
}
```

4. Call in your backend like this:
```python
# Python
import requests

username = 'team-oomf'
password = 'hunter2'
token = base64.b64encode(f'{username}:{password}'.encode('ascii')).decode('utf-8')
header = {'HTTP_AUTHORIZATION': f'Basic {token}'}
# todo(turnip): change when we have actual domain
response = requests.get('http://sociocon.herokuapp.com/remote-node/', **headers)
```

### How to add a remote node in the server: Troubleshooting

- **401**: You're not logged in.
- **403**: You're either logging in as a user or your node has been deactivated.
- **404**: Wrong url. Try adding a slash at the end? Double-check your format.
