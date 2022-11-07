# Remote Node

Remote nodes are just normal users with a special hidden type. It can be activated and reactivated by the server admin.

## Setup: How to add a remote node in the server

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

- Note: you cannot make this in `admin/`, because the password is encrypted!

2. In `admin/`, make sure that the **Author type**: is **Active Remote Node**
3. Test out Basic Auth by calling this endpoint:

```shell
# curl local
curl http://team-oomf:hunter2@127.0.0.1:8000/remote-node/

# curl remote
# todo(turnip): change when we have actual domain
curl http://team-oomf:hunter2@www.sociocon.herokuapp.com/remote-node/

# alternatively: httpie
http -a team-oomf:hunter2 http://www.sociocon.herokuapp.com/remote-node/
````

If you want to try it in your browser: [http://team-oomf:hunter2@127.0.0.1:8000/remote-node/](http://team-oomf:hunter2@127.0.0.1:8000/remote-node/)

**Warning: remember to logout from your admin or clear current cookies or local storage!**

The result should look like:

```json
{
  "message": "Authentication passed!",
  "type": "remoteNode"
}
```
