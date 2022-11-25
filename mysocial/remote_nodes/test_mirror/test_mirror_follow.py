import json
import os

import requests
from django.test import TestCase
from requests import ConnectionError


class TestSession:
    """
    Automated testing for our servers mirrored.

    The tests below will pretend to be a user in a browser, following each other.

    To run:
    1. Run this server in 8000 and 8080
    2. From manage.py's directory:
        python manage.py test remote_nodes/test_mirror/
    """

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
    def setUp(self):
        redirection = os.environ.get('MYSOCIAL_TEST_REDIRECTION')
        redirection = './' if redirection is None else redirection
        os.system(f"python {redirection}manage.py cleartest")
        self.local = TestSession(('actor', 'actor'), 'http://127.0.0.1:8000')
        self.remote = TestSession(('target', 'target'), 'http://127.0.0.1:8080')

    def test_all(self):
        self.follow_flow_happy_path()
        self.follow_flow_decline()

    def follow_flow_happy_path(self):
        # local actor checks if they already requested remote target (404)
        try:
            response = self.local.session.get(
                f'{self.local.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        except ConnectionError as err:
            print("8000 and 8080 servers were not detected. Please run them before running this test.")
            raise err
        self.assertEqual(response.status_code, 404)

        # local actor follows remote target
        response = self.local.session.post(f'{self.local.base}/authors/{self.remote.author_id}/followers/')
        content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200, content)

        # # target receives follow request
        response = self.remote.session.get(f'{self.remote.base}/follows/incoming')
        self.assertEqual(response.status_code, 200)
        found = False
        for follow_request in json.loads(response.content)['items']:
            if follow_request['actor']['id'] == self.local.author_id:
                found = True
                break
        self.assertTrue(found)

        # local checks if target has accepted their request (404)
        response = self.local.session.get(
            f'{self.local.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 404)

        # target accepts the follow request
        response = self.remote.session.put(
            f'{self.remote.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}',
            data={'hasAccepted': True}
        )
        content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200, content)

        # local checks if target has accepted their request (200)
        response = self.local.session.get(
            f'{self.local.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 200)

        # double accept! (400)
        response = self.remote.session.put(
            f'{self.remote.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}',
            data={'hasAccepted': True}
        )
        self.assertEqual(response.status_code, 200)

        # see if follower
        response = self.local.session.get(f'{self.local.base}/authors/{self.remote.author_id}/followers/')
        found = False
        for follow_request in json.loads(response.content)['items']:
            if follow_request['id'] == self.local.author_id:
                found = True
                break
        self.assertTrue(found)

        # just kidding! i wanna unfollow now >.>
        response = self.local.session.delete(
            f'{self.local.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 200)

        # local actor checks if they are following (404)
        response = self.local.session.get(
            f'{self.local.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 404)

        # remote target checks if these author is following (404)
        response = self.remote.session.get(
            f'{self.remote.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 404)

        # see if follower (should be not)
        response = self.local.session.get(f'{self.local.base}/authors/{self.remote.author_id}/followers/')
        found = False
        for follow_request in json.loads(response.content)['items']:
            if follow_request['id'] == self.local.author_id:
                found = True
                break
        self.assertFalse(found)

    def follow_flow_decline(self):
        # local actor follows remote target
        response = self.local.session.post(f'{self.local.base}/authors/{self.remote.author_id}/followers/')
        content = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200, content)

        response = self.remote.session.delete(
            f'{self.remote.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 200)

        # local actor checks if they are following (404)
        response = self.local.session.get(
            f'{self.local.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 404)

        # remote target checks if these author is following (404)
        response = self.remote.session.get(
            f'{self.remote.base}/authors/{self.remote.author_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 404)
