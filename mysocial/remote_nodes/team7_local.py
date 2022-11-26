import json
import urllib.parse
import urllib.parse

import requests

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
            response = requests.get(url, auth=(self.username, self.password))
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
                else:
                    for err in author_deserializer.errors:
                        print(f'{self}: get_all_author_jsons: {err}')
            return author_list
        return None
