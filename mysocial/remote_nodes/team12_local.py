import json
import urllib.parse

import requests
from rest_framework import status
from rest_framework.response import Response

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from common.base_util import BaseUtil
from common.pagination_helper import PaginationHelper
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer
from mysocial.settings import base
from post.serializer import PostSerializer
from remote_nodes.local_default import LocalDefault


class Team7Local(LocalDefault):
    domain = '127.0.0.1:8012'
    username = 'team7_local'
    team_metadata_tag = 'team7'

    """Mapping: remote <-> local"""
    remote_author_fields = {
        'id': 'official_id',
        # todo: map username to username too?
        'username': 'display_name',
        'github': 'github',
        'profile_image': 'profile_image'
    }

    def __init__(self):

        """
        To use headers:
            response = requests.get('url',
                                    headers=self.headers,
                                    auth=(self.username, self.password))
        """
        self.bearer_token = None

        super().__init__()

    @classmethod
    def create_node_credentials(cls):
        """This is for local testing"""
        return {
            cls.domain: {
                'username': 'team10_local@mail.com',
                'password': 'team10_local',
                'remote_username': 'local_default',
                'remote_password': 'local_default',
            }
        }

    @property
    def headers(self):
        """
        Use like:
            response = requests.get(url, headers=self.headers)
        """
        return {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4NTE1Nzg2LCJpYXQiOjE2Njk4NzU3ODYsImp0aSI6ImRjZDVjNzVmZThiODQxNTFiZjVlMTY4Y2QxNTMyNTA4IiwidXNlcl9lbWFpbCI6InRlYW0xMEBtYWlsLmNvbSJ9.szjZU1nF4vIenkWxA_IiJ8rOMM7m2ow1qZgzciKGO-k'
        }

    def get_all_author_jsons(self, params: dict):
        """Returns a list of authors as json"""
        url = f'{self.get_base_url()}/authors/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param

        try:
            response = requests.get(url, headers=self.headers)
        except ConnectionError as e:
            print(f"{self.__class__.username}: url ({url}) Connection error: {e}")
            return None
        except Exception as e:
            print(f"{self.__class__.username}: Unknown err: {e}")
            return None

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            author_list = []
            for raw_author in author_json['items']:
                raw_author['url'] = url  # since we don't trust their url; this works
                author_deserializer = AuthorSerializer(data=raw_author)
                if author_deserializer.is_valid():
                    author = author_deserializer.validated_data
                    author_list.append(AuthorSerializer(author).data)
            return author_list
        return None

    def get_author_via_url(self, author_url: str) -> Author:
        raise NotImplementedError()
        response = requests.get(author_url)  # no password

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            author_json['url'] = author_url  # since we don't trust their url; this works
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None
