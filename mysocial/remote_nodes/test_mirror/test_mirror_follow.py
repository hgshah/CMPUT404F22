import json

import requests
from django.test import TestCase

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer


class TestSession:
    def __init__(self, auth: (str, str), base='http://127.0.0.1:8000'):
        self.auth = auth
        self.base = base
        self.session = requests.Session()
        self.session.auth = self.auth
        response = self.session.get(f'{self.base}/authors/self/')
        self.content = json.loads(response.content.decode('utf-8'))
        self.author_id = self.content['id']
        self.author_id = self.content['id']


class TestMirrorFollow(TestCase):
    def test_follow_flow_happy_path(self):
        # todo: delete Follow entries for both mirror and local to test this out

        local = TestSession(('actor', 'actor'), 'http://127.0.0.1:8000')
        remote = TestSession(('target', 'target'), 'http://127.0.0.1:8080')

        # local actor checks if they already requested remote target (404)
        response = local.session.get(f'{local.base}/authors/{remote.author_id}/followers/{local.author_id}')
        self.assertEqual(response.status_code, 404)

        # local actor follows remote target
        response = local.session.post(f'{local.base}/authors/{remote.author_id}/followers/')
        self.assertEqual(response.status_code, 200)

        # # target receives follow request
        response = remote.session.get(f'{remote.base}/follows/incoming')
        self.assertEqual(response.status_code, 200)
        found = False
        for follow_request in json.loads(response.content)['items']:
            if follow_request['actor']['id'] == local.author_id:
                found = True
                break
        self.assertTrue(found)

        # local checks if target has accepted their request (404)
        response = local.session.get(f'{local.base}/authors/{remote.author_id}/followers/{local.author_id}')
        self.assertEqual(response.status_code, 404)

        # target accepts the follow request
        response = remote.session.put(
            f'{remote.base}/authors/{remote.author_id}/followers/{local.author_id}',
            data={'hasAccepted': True}
        )
        self.assertEqual(response.status_code, 200)

        # local checks if target has accepted their request (200)
        response = local.session.get(f'{local.base}/authors/{remote.author_id}/followers/{local.author_id}')
        self.assertEqual(response.status_code, 200)

        # delete!
        response = remote.session.put(
            f'{remote.base}/authors/{remote.author_id}/followers/{local.author_id}',
            data={'hasAccepted': True}
        )
        self.assertEqual(response.status_code, 200)