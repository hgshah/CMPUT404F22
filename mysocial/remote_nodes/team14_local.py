import json
import urllib.parse

import requests

from authors.serializers.author_serializer import AuthorSerializer
from remote_nodes.local_default import LocalDefault


class Team14Local(LocalDefault):
    domain = '127.0.0.1:8014'
    username = 'team14_local'
    remote_author_fields = {
        'id': 'official_id',
        'url': 'url',
        'display_name': 'display_name',
        'github_handle': 'github',
        'profile_image': 'profile_image'
    }

    def get_base_url(self):
        return f'http://{self.__class__.domain}/api'

    @classmethod
    def create_node_credentials(cls):
        return {
            cls.domain: {
                'username': 'team14_local',
                'password': 'team14_local',
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
        except ConnectionError:
            return None
        except Exception as e:
            print(f"Team14Local: Unknown err: {e}")
            return None

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            author_list = []
            for raw_author in author_json:
                author_deserializer = AuthorSerializer(data=raw_author)
                if author_deserializer.is_valid():
                    author = author_deserializer.validated_data
                    author_list.append(AuthorSerializer(author).data)
                else:
                    for err in author_deserializer.errors:
                        print(f'{self}: get_all_author_jsons: {err}')
            return author_list
        return None
