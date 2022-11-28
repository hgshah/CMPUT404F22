import json
import os
import uuid

import requests
from django.test import TestCase
from requests import ConnectionError


class TestSession:
    """
    Automated testing for our servers mirrored.

    The tests below will pretend to be a user in a browser, following each other.

    To run:
    1. Run this server in 8000 and and team14's server in 8014
    2. From manage.py's directory:
        python manage.py test remote_nodes/test_team14/
    """

    def __init__(self, auth: (str, str), base='http://127.0.0.1:8000'):
        self.auth = auth
        self.base = base
        self.session = requests.Session()
        self.session.auth = self.auth
        response = self.session.get(f'{self.base}/authors/self/')
        self.content = json.loads(response.content.decode('utf-8'))
        self.author_id = self.content['id']


class TestTeam14Follow(TestCase):
    def setUp(self):
        redirection = os.environ.get('MYSOCIAL_TEST_REDIRECTION')
        redirection = './' if redirection is None else redirection
        os.system(f"python {redirection}manage.py cleartest")
        self.local = TestSession(('actor', 'actor'), 'http://127.0.0.1:8000')
        # todo: make instructions for testing this one
        self.remote_id = str(uuid.UUID('739252c2b11e4fe8bb96b57b939a8331'))

    def test_all(self):
        self.follow_flow_happy_path()
        self.check_if_follow()

    def follow_flow_happy_path(self):
        # local actor checks if they already requested remote target (404)
        try:
            response = self.local.session.get(
                f'{self.local.base}/authors/{self.remote_id}/followers/{self.local.author_id}')
        except ConnectionError as err:
            print("8000 and 8080 servers were not detected. Please run them before running this test.")
            raise err
        self.assertEqual(response.status_code, 404)

        # local actor follows remote target
        response = self.local.session.post(f'{self.local.base}/authors/{self.remote_id}/followers/')
        content = response.content.decode('utf-8')
        if response.status_code != 201:
            print(content)
        self.assertEqual(response.status_code, 201, content)

        # they have to accept it on their end >.>, so there's nothing here

    def check_if_follow(self):
        # this is the case when they accept it on their end
        response = self.local.session.get(
            f'{self.local.base}/authors/{self.remote_id}/followers/{self.local.author_id}')
        self.assertEqual(response.status_code, 200)
