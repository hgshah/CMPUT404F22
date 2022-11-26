import json
import urllib.parse
import urllib.parse

import requests

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from common.base_util import BaseUtil
from remote_nodes.local_default import LocalDefault


class Team7Local(LocalDefault):
    domain = '127.0.0.1:8007'
    username = 'team7_local'
    team_metadata_tag = 'team7'

    """Mapping: remote <-> local"""
    remote_author_fields = {
        'id': 'official_id',
        # WARNING: DO NOT TRUST THEIR URL!!!
        'displayName': 'display_name',
        'github': 'github',
        'profileImage': 'profile_image'
    }

    def get_base_url(self):
        return f'{BaseUtil.get_http_or_https()}{self.__class__.domain}/service'

    @classmethod
    def create_node_credentials(cls):
        """This is for local testing"""
        return {
            cls.domain: {
                'username': 'team7_local',
                'password': 'team7_local',
                'remote_username': 'local_default',
                'remote_password': 'local_default',
            }
        }

    def get_all_author_jsons(self, params: dict):
        """Returns a list of authors as json"""
        url = f'{self.get_base_url()}/authors/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param

        try:
            response = requests.get(url)
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
                author_deserializer = AuthorSerializer(data=raw_author)
                if author_deserializer.is_valid():
                    author = author_deserializer.validated_data
                    author_list.append(AuthorSerializer(author).data)
            return author_list
        return None

    def get_author_via_url(self, author_url: str) -> Author:
        response = requests.get(author_url)  # no password

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None

    def get_author_via_url(self, author_url: str) -> Author:
        response = requests.get(author_url)  # no password

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None
