import json

import requests
from django.http import HttpResponseNotFound
from django.utils.baseconv import base64
from rest_framework.response import Response

from mysocial.settings import base


class NodeConfigBase:
    """
    Sample and base config

    Remember to call super whenever possible; use good judgment to determine when to call super in the method body.
    """

    # todo(turnip): check entry in Author, if does not exist, make one

    """
    Call domain with self.__class__.domain so you can override it in classes that inherit this.
    Inheriting classes may not need it unless when needed
    """
    domain = 'domain.herokuapp.com'

    def __init__(self):
        if base.CURRENT_DOMAIN == '127.0.0.1:8000':
            self.username = 'username'
            self.password = 'password'
            return

        credentials = base.REMOTE_CONFIG_CREDENTIALS[self.__class__.domain]
        self.username = credentials['username']
        self.password = credentials['password']
        # todo(turnip): check entry in Author, check if inactive?

    @classmethod
    def create_dictionary_entry(cls):
        return {cls.domain: cls()}

    # endpoints
    def get_all_authors_request(self):
        response = requests.get(f'http://{self.__class__.domain}/authors/')
        if response.status_code == 200:
            # todo(turnip): map to our author?
            return Response(json.loads(response.content))
        return HttpResponseNotFound()

    def get_author_request(self, author_id: str):
        response = requests.get(f'http://{self.__class__.domain}/authors/{author_id}/')
        if response.status_code == 200:
            # todo(turnip): map to our author?
            return Response(json.loads(response.content))
        return HttpResponseNotFound()

    def get_author(self, author_url: str):
        token = base64.b64encode(f'{self.username}:{self.password}'.encode('ascii')).decode('utf-8')
        headers = {'HTTP_AUTHORIZATION': f'Basic {token}'}
        response = requests.get(author_url, **headers)

        if response.status_code == 200:
            # todo(turnip): map to our author?
            return response.data
        else:
            return None
