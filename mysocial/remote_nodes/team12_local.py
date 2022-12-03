import json
import urllib.parse

import requests

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from remote_nodes.local_default import LocalDefault


class Team12Local(LocalDefault):
    domain = '127.0.0.1:8012'
    username = 'team12_local'
    team_metadata_tag = 'team12'

    """Mapping: remote <-> local"""
    remote_author_fields = {
        'id': 'official_id',
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
                'username': cls.username,
                'password': 'team12_local',
                'remote_username': 'local_default@mail.com',
                'remote_password': 'local_default',
            }
        }

    def get_headers(self):
        """
        Use like:
            response = requests.get(url, headers=self.headers)
        """
        if self.bearer_token is None:
            try:
                payload = json.dumps({
                    "email": self.username,
                    "password": self.password
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                response = requests.post(
                    f'{self.get_base_url()}/api/auth/token/obtain/',
                    data=payload,
                    headers=headers)
                if response.status_code == 200:
                    response_json: dict = json.loads(response.text)
                    self.bearer_token = response_json.get('access')
            except ConnectionError as err:
                print(f'{self}: headers: connection error: the other server at {self.get_base_url()} may not be up or '
                      f'too slow to respond')
            except Exception as e:
                print(f'{self}: headers: unknown error: {e}')

        if self.bearer_token is None:
            print(f'{self}: headers: bearer token still empty')

        return {
            'Authorization': f'Bearer {self.bearer_token}'
        }

    def get_all_author_jsons(self, params: dict):
        """Returns a list of authors as json"""
        url = f'{self.get_base_url()}/authors/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param

        try:
            response = requests.get(url, headers=self.get_headers())
        except ConnectionError:
            print(f'Connection error: {self}')
            return None
        except Exception as e:
            print(f"NodeConfigBase: Unknown err: {str(e)}")
            return None

        if response.status_code == 200:
            return AuthorSerializer.deserializer_author_list(response.content.decode('utf-8'))
        return None

    def get_author_via_url(self, author_url: str) -> Author:
        response = requests.get(author_url, headers=self.get_headers())

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            author_json['url'] = author_url  # since we don't trust their url; this works
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None
