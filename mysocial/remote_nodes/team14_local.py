import json

import requests
import urllib.parse
from rest_framework.response import Response
from rest_framework import status

from authors.serializers.author_serializer import AuthorSerializer
from common.base_util import BaseUtil
from remote_nodes.local_default import LocalDefault
from authors.models.author import Author
from post.models import Post
from post.serializer import PostSerializer
from rest_framework import status

from common.pagination_helper import PaginationHelper

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

    post_remote_fields = {
        'id': 'official_id',
        'url': 'url',
        "title": "title",
        "source": "source",
        "origin": "origin",
        "description": "description",
        "content_type": "contentType",
        "author": "author",
        "created_at": "published",
        "visibility": "visibility",
        "unlisted": "unlisted"
    } 

    def get_base_url(self):
        return f'{BaseUtil.get_http_or_https()}{self.__class__.domain}/api'

    @classmethod
    def create_node_credentials(cls):
        """This is for local testing"""
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

    def get_authors_posts(self, request, author_post_path: str):
        url = f'{self.get_base_url()}{author_post_path}'

        try:
            response = requests.get(url, auth=(self.username, self.password))
        except Exception as e:
            return Response(f"Failed to get author's post from remote server, error: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = []
        post_data = json.loads(response.content.decode('utf-8'))
        for post in post_data:
            data.append(self.convert_team14_post(url, post))

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return Response(err, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': 'posts', 'items': data}, status = status.HTTP_200_OK)

    def convert_team14_post(self, url, post_data):
        post_data["url"] = url 
        
        serializer = PostSerializer(data = post_data)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors
