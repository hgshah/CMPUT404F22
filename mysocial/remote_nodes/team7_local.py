import json
import urllib.parse
import urllib.parse

import requests
from common.pagination_helper import PaginationHelper
import requests
import urllib.parse
from rest_framework.response import Response
from rest_framework import status

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from common.base_util import BaseUtil
from mysocial.settings import base
from remote_nodes.local_default import LocalDefault
from post.serializer import PostSerializer


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

    post_remote_fields = {
        "type": "type",
        '_id': 'official_id',
        'url': 'url',
        "title": "title",
        "source": "source",
        "origin": "origin",
        "description": "description",
        "contentType": "contentType",
        "author": "author",
        "created_at": "published",
        "visibility": "visibility",
        "unlisted": "unlisted",
        "categories": "categories",
        "count": "count",
        "comments": "comments",
        "visibility": "visibility",
        "unlisted": "unlisted",
        "published": "published",
    }

    def __init__(self):

        """
        To use headers:
            response = requests.get('url',
                                    headers=self.headers,
                                    auth=(self.username, self.password))
        """
        self.origin = f'{BaseUtil.get_http_or_https()}{base.CURRENT_DOMAIN}'
        self.headers = {
            'Origin': self.origin,
        }

        super().__init__()

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
                raw_author['url'] = url  # since we don't trust their url; this works
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
            author_json['url'] = author_url  # since we don't trust their url; this works
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None

    def get_author_via_url(self, author_url: str) -> Author:
        response = requests.get(author_url)  # no password

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            author_json['url'] = author_url  # since we don't trust their url; this works
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None

    def get_authors_posts(self, request, author_post_path: str):
        url = f'{self.get_base_url()}{author_post_path}'

        try:
            response = requests.get(url, auth=(self.username, self.password))
            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get author's  post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(f"Failed to get author's post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = []
        
        post_data = json.loads(response.content.decode('utf-8'))
        for key, value in post_data.items():
            data.append(self.convert_team7_post(url, value))

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': 'posts', 'items': data}, status=status.HTTP_200_OK)


    def convert_team7_post(self, url, post_data):
        post_data["url"] = url

        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors
    