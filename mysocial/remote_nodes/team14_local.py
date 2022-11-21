import json

import requests

from remote_nodes.local_default import LocalDefault


class Team14Local(LocalDefault):
    domain = '127.0.0.1:8014'
    username = 'team14_local'
    remote_fields = {
        'id': 'official_id',
        'url': 'url',
        'display_name': 'display_name',
        'github': 'github',
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
        except ConnectionError as e:
            print(f"{self.__class__.username}: url ({url}) Connection error: {e}")
            return None
        except Exception as e:
            print(f"{self.__class__.username}: Unknown err: {e}")
            return None

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print(f'Invalid response code: {response.status_code}')
            message = response.content.decode('utf-8')
            print(f'Invalid response code: {message}')

        return None
