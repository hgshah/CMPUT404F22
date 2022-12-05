import json
import urllib.parse

import requests
from django.http import HttpResponseNotFound
from rest_framework.response import Response
from requests import ConnectionError
from rest_framework import status

from authors.models.author import Author
from authors.models.remote_node import NodeStatus
from authors.serializers.author_serializer import AuthorSerializer
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer
from common.base_util import BaseUtil


class NodeConfigBase:
    """
    Serves as sample and base configuration for remote server/node specific implementations

    Remember to call super whenever possible; use good judgment to determine when to call super in the method body.
    """

    """
    Call domain with self.__class__.domain so you can override it in classes that inherit this.
    Inheriting classes may not need it unless when needed
    """
    domain = 'domain.herokuapp.com'
    username = 'domain'
    team_metadata_tag = 'default'
    author_serializer = AuthorSerializer

    """
    Mapping: remote to local
    
    Check author_serializer.py for duplicate; can't ref due to circular dependency
    """
    remote_author_fields = {
        'id': 'official_id',
        'url': 'url',
        'host': 'host',
        'displayName': 'display_name',
        'github': 'github',
        'profileImage': 'profile_image'
    }
    remote_follow_fields = {
        'id': 'proxy_id',  # fake; for serializer
        'hasAccepted': 'has_accepted',
        'object': 'target',
        'actor': 'actor',
        'localUrl': 'local_url',  # fake; for serializer
        'remoteUrl': 'proxy_url'  # fake; for serializer
    }

    def __init__(self):
        self.is_valid = False
        try:
            self.node_author = Author.objects.get(username=self.username)
            self.node_detail = self.node_author.node_detail
            if self.node_detail.status != NodeStatus.ACTIVE:
                # if we set inactive, don't include!
                print(f'Node author is deactivated: {self.username}: {self.__class__}')
                return

            self.username = self.node_detail.remote_username
            self.password = self.node_detail.remote_password
            self.is_valid = True
        except Exception as e:
            print(f'Node author does not exist yet...: Finding username {self.username} {self.__class__}): {e}')

    @classmethod
    def create_dictionary_entry(cls):
        result = cls()
        if result.is_valid:
            print(f"Adding node: {result.username}")
            return {cls.domain: result}
        else:
            # prevent adding invalid classes
            print(f"Removing node: {result.username}")
            return {}

    def get_base_url(self):
        return f'{BaseUtil.get_http_or_https()}{self.__class__.domain}'

    def convert_to_valid_author_url(self, author_id: str) -> str:
        return f'{self.get_base_url()}/authors/{author_id}'

    def get_all_author_jsons(self, params: dict):
        """Returns a list of authors as json"""
        url = f'{self.get_base_url()}/authors/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param

        try:
            response = requests.get(url, auth=(self.username, self.password))
        except ConnectionError:
            print(f'Connection error: {self}')
            return None
        except Exception as e:
            print(f"NodeConfigBase: Unknown err: {str(e)}")
            return None

        if response.status_code == 200:
            return AuthorSerializer.deserializer_author_list(response.content.decode('utf-8'))
        return None

    # endpoints
    def get_all_authors_request(self, params: dict):
        """Returns all authors as a valid HTTP Response"""
        author_jsons = self.get_all_author_jsons(params)

        if author_jsons is None:
            return HttpResponseNotFound()
        return Response({
            "type": "authors",
            "items": author_jsons
        })

    # todo: double check this is no longer used
    def from_author_id_to_url(self, author_id: str) -> str:
        url = f'{self.get_base_url()}/authors/{author_id}/'
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            # todo(turnip): map to our author?
            json_dict = json.loads(response.content)
            return json_dict['url']
        return None

    def from_author_id_to_author(self, author_id: str) -> Author:
        url = f'{self.get_base_url()}/authors/{author_id}/'
        return self.get_author_via_url(url)

    # todo: double check this is no longer used
    def get_author_request(self, author_id: str):
        response = requests.get(f'{self.get_base_url()}/authors/{author_id}/', auth=(self.username, self.password))
        if response.status_code == 200:
            # todo(turnip): map to our author?
            return Response(json.loads(response.content))
        return HttpResponseNotFound()

    def get_author_via_url(self, author_url: str) -> Author:
        response = requests.get(author_url, auth=(self.username, self.password))

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None

    def get_all_followers(self, author: Author, params=None):
        if params is None:
            # python has a weird property that if the argument is mutable, like a dictionary
            # if you pass the reference around, you can actually change the default values,
            # like params here. doing this to prevent evil things
            params = {}

        url = f'{author.get_url()}/followers/'
        if len(params) > 0:
            query_param = urllib.parse.urlencode(params)
            url += '?' + query_param
        response = requests.get(url, auth=(self.username, self.password))
        if response.status_code == 200:
            return AuthorSerializer.deserializer_author_list(response.content.decode('utf-8'))
        return None

    def get_all_followers_request(self, author: Author, params: dict):
        followers = self.get_all_followers(author=author, params=params)
        if followers is not None:
            return Response({
                "type": "followers",
                "items": followers
            })
        return HttpResponseNotFound()

    def post_local_follow_remote(self, author_actor: Author, author_target: Author) -> dict:
        """Make call to remote node to follow"""
        url = f'{author_target.get_url()}/followers/'
        response = requests.post(url,
                                 auth=(self.username, self.password),
                                 data={'actor': author_actor.get_url()})
        if 200 <= response.status_code < 300:
            try:
                return json.loads(response.content.decode('utf-8'))
            except Exception as e:
                print(f"Failed to deserialize response: {response.content}")
        else:
            print(f"post_local_follow_remote: remote server response: {response.status_code}")
        return response.status_code

    def delete_local_follow_remote(self, author_target: Author, author_actor: Author) -> dict:
        """Make call to remote node to delete follow; stop sending stuff in my inbox!!!"""
        url = f'{author_target.get_url()}/followers/{author_actor.get_id()}'
        response = requests.delete(url,
                                   auth=(self.username, self.password))
        if 200 <= response.status_code < 300:
            try:
                return json.loads(response.content.decode('utf-8'))
            except Exception as e:
                print(f"Failed to deserialize response: {response.content}")
        else:
            print(f"post_local_follow_remote: remote server response: {response.status_code}")
        return response.status_code

    def get_remote_follow(self, target: Author, follower: Author) -> Follow:
        """
        Make call to remote node to get a follow object or request

        Returns a Follow object if there is one;
        Returns None if cannot be found
        """
        url = f'{target.get_url()}/followers/{follower.get_id()}'
        response = requests.get(url, auth=(self.username, self.password))
        if 200 <= response.status_code < 300:
            follow_json = json.loads(response.content)
            follow_serializer = FollowRequestSerializer(data=follow_json)
            if not follow_serializer.is_valid():
                for err in follow_serializer.errors:
                    print(f'NodeConfigBase: get_remote_follow: serialization error: {err}')
                return None
            return follow_serializer.validated_data
        else:
            print(f'NodeConfigBase: get_follow_request: get failed: {response.status_code}')
            return None

    def send_to_remote_inbox(self, data, target_author_url):
        if target_author_url is None:
            return 404
        url = f'{target_author_url}/inbox'
        return requests.post(url = url, data = json.dumps(data), auth = (self.username, self.password), headers = {'content-type': 'application/json'})

    def get_authors_liked_on_post(self, object_id):
        url = f'{self.get_base_url()}{object_id}'
        return requests.get(url = url, auth = (self.username, self.password))

    def get_authors_liked_on_comment(self, object_id):
        url = f'{self.get_base_url()}{object_id}'
        return requests.get(url = url, auth = (self.username, self.password))

    def get_authors_likes(self, target_author_url):
        url = f'{target_author_url}/liked'
        return requests.get(url = url, auth = (self.username, self.password))

    def get_post_by_post_id(self, post_url):
        url = f'{self.get_base_url()}{post_url}'
        response =  requests.get(url = url, auth = (self.username, self.password))

        if response.status_code < 200 or response.status_code > 300:
            return Response("Failed to get post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(json.loads(response.content), status = status.HTTP_200_OK)

    def get_authors_posts(self, request, author_posts_path):
        url = f'{self.get_base_url()}{author_posts_path}'
        response = requests.get(url = url, auth = (self.username, self.password))
        
        if response.status_code < 200 or response.status_code > 300:
            return Response("Failed to get author's post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(json.loads(response.content), status = status.HTTP_200_OK)

    def get_comments_for_post(self, comments_path):
        url = f'{self.get_base_url()}{comments_path}'
        return requests.get(url = url, auth = (self.username, self.password))
    
    def create_comment_on_post(self, comments_path, data):
        url = f'{self.get_base_url()}{comments_path}'
        return requests.post(url = url, data = json.dumps(data), auth = (self.username, self.password), headers = {'content-type': 'application/json'})
