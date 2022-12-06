import json
import urllib.parse

import requests
import urllib.parse
from rest_framework.response import Response
from rest_framework import status

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from common.base_util import BaseUtil
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer
from remote_nodes.local_default import LocalDefault
from post.serializer import PostSerializer
from rest_framework import status
from comment.serializers import CommentSerializer

from common.pagination_helper import PaginationHelper


class Team14Local(LocalDefault):
    domain = '127.0.0.1:8014'
    username = 'team14_local'

    """team14 fields <-> our fields"""
    remote_author_fields = {
        'id': 'official_id',
        'url': 'url',
        'display_name': 'display_name',
        'github_handle': 'github',
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
        "unlisted": "unlisted",
        "content": "content"
    }

    comment_remote_fields = {
        "id": "url",
        "type": "type",
        "author": "author",
        "comment": "comment",
        "content_type": "contentType",
        "created_at": "published",
        "official_id": "official_id"
    }

    def get_base_url(self):
        return f'{BaseUtil.get_http_or_https()}{self.__class__.domain}/api'

    def convert_to_valid_author_url(self, author_id: str) -> str:
        return f'{self.get_base_url()}/authors/{author_id}'

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

    def post_local_follow_remote(self, author_actor: Author, author_target: Author) -> dict:
        url = f'{author_target.get_url()}/inbox/'
        response = requests.post(url,
                                 auth=(self.username, self.password),
                                 json={
                                     'type': 'follow',
                                     'sender': {
                                         'url': author_actor.get_url(),
                                         'id': author_actor.get_id()
                                     },
                                     'receiver': {
                                         'url': author_target.get_url(),
                                         'id': author_target.get_id(),
                                     }
                                 })
        if 200 <= response.status_code < 300:
            return {
                'type': 'follow',
                'actor': {'url': author_actor.get_url()},
                'object': {'url': author_target.get_url()},
                'hasAccepted': False,
                'localUrl': f'{author_actor.get_url()}/followers/{author_target.get_id()}/',
                'id': None
            }  # <- GOOD
        print(f'{self}: post_local_follow_remote: {response.content}')
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
            if 'message' not in follow_json or follow_json['message'] != 'follower indeed':
                print(f'{self}: get_remote_follow: unknown message: {follow_json}')
                return None

            follow_serializer = FollowRequestSerializer(data={
                'actor': AuthorSerializer(follower).data,
                'object': AuthorSerializer(target).data,
                'hasAccepted': True,  # team14 returns a message that says follower indeed if you're a follower
                'localUrl': url,
                'id': None
            })
            if not follow_serializer.is_valid():
                for err in follow_serializer.errors:
                    print(f'{self}: get_remote_follow: serialization error: {err}')
                return None
            return follow_serializer.validated_data
        else:
            print(f'{self}: get_follow_request: get failed: {response.status_code}')
            return None

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
            return AuthorSerializer.deserializer_author_list(response.content.decode('utf-8'))
        else:
            print(f'Non-200 status code for team 14: {url}')
            print(response.content.decode('utf-8'))
        return None

    def get_authors_posts(self, request, author_post_path: str):
        url = f'{self.get_base_url()}{author_post_path}'

        try:
            response = requests.get(url, auth=(self.username, self.password))
            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get author's  post from remote server",
                                status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(f"Failed to get author's post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = []
        post_data = json.loads(response.content.decode('utf-8'))
        for post in post_data:
            data.append(self.convert_team14_post(url, post))

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': 'posts', 'items': data}, status=status.HTTP_200_OK)

    def get_post_by_post_id(self, post_url: str):
        url = f'{self.get_base_url()}{post_url}'

        try:
            response = requests.get(url, auth=(self.username, self.password))

            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(f"Failed to get author's post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        post_data = json.loads(response.content.decode('utf-8'))

        post = self.convert_team14_post(url, post_data)
        return Response(post, status=status.HTTP_200_OK)

    def send_to_remote_inbox(self, data, target_author_url):
        if target_author_url is None:
            return 404
        url = f'{target_author_url}/inbox/'

        data = self.convert_post_in_inbox(data)
        response = requests.post(url=url, data=json.dumps(data), auth=(self.username, self.password),
                                 headers={'content-type': 'application/json'})

        if response.status_code < 200 or response.status_code > 300:
            return Response(f"Failed to get post from remote server, error {json.loads(response.content)}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("Successfully sent to remote inbox!", status=status.HTTP_200_OK)

    def get_comments_for_post(self, comments_path, author = None, request = None):
        url = f'{self.get_base_url()}{comments_path}/'

        try:
            response = requests.get(url, auth=(self.username, self.password))
            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get comments for post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response(f"Failed to get comments for post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = []
        comment_data = json.loads(response.content.decode('utf-8'))
        
        for comment in comment_data:
            data.append(self.convert_team14_comment(comment))
        
        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': 'posts', 'items': data}, status=status.HTTP_200_OK)

    def create_comment_on_post(self, comments_path, data, extra_data = None):
        author_url = extra_data['post']['post']['author']['url']
        url = f'{author_url}/inbox/'
        data = self.create_team14_comment(data, extra_data)
        response = requests.post(url = url, data = json.dumps(data), auth = (self.username, self.password), headers = {'content-type': 'application/json'})
        if response.status_code < 200 or response.status_code > 300:
            return Response(
                f"Failed to get post from remote server, error {json.loads(response.content)}",
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("Successfully created comment to team 14!", status=status.HTTP_200_OK)
    
    def get_authors_liked_on_post(self, object_id):
        url = f'{self.get_base_url()}{object_id}'
        response =  requests.get(url = url, auth = (self.username, self.password))

        if response.status_code < 200 or response.status_code > 300:
            return Response("Failed to get author likes for post on remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        team14_authors = json.loads(response.content.decode('utf-8'))
        data = []
        for author in team14_authors:
            converted_author = self.convert_team14_authors(url, author)
            data.append(converted_author)
        
        return Response(data, status = status.HTTP_200_OK)
    
    def like_a_post(self, data, target_author_url, extra_data = None):
        url = f'{target_author_url}/inbox/'
        data = self.create_team14_like_post(data, target_author_url)
        response = requests.post(url = url, data = json.dumps(data), auth = (self.username, self.password), headers = {'content-type': 'application/json'})
        
        if response.status_code < 200 or response.status_code > 300:
            return Response(
                f"Failed to like post on team 14, error {json.loads(response.content)}",
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("Successfully created like to team 14!", status=status.HTTP_200_OK)

    def convert_team14_post(self, url, post_data):
        post_data["url"] = url

        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors
    
    def convert_team14_authors(self, url, author_data):
        author_data["url"] = url

        serializer = AuthorSerializer(data=author_data)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors
    
    def convert_team14_comment(self, comment_data):
        team14_comment_id = comment_data['id'].split('comments/')[1].rstrip("/")
        comment_data['official_id'] = team14_comment_id

        url = comment_data['id']
        comment_data['url'] = url
        
        serializer = CommentSerializer(data = comment_data)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors

    def convert_post_in_inbox(self, data):
        inbox_post = {
            "type": "post",
            "post": {
                "id": "",
                "author": {
                    "id": "",
                    "url": ""
                }
            }
        }

        inbox_post['post']['id'] = data['id']
        inbox_post['post']['author']['id'] = data['author']['id']
        inbox_post['post']['author']['url'] = data['author']['url']
        return inbox_post

    def create_team14_comment(self, data, extra_data):
        comment = {
            "type": "comment",
            "comment": "",
            "content_type": "",
            "author": {
                "id": "",
                "url": ""
            },
            "post": {
                "id": "",
                "author": {
                    "id": "",
                    "url": ""
                }
            }
        }

        comment['comment'] = data['comment']
        comment['content_type'] = data['contentType']
        comment['author']['url'] = data['actor']
        comment['author']['id'] = data['actor'].split('authors/')[1]
        comment.update(extra_data['post'])
        return comment

    def create_team14_like_post(self, data, target_author_url):
        like = {
            "type": "like",
            "author": {
                "id": "",
                "url": ""
            },
            "post": {
                "id": "",
                "author": {
                "id": "",
                "url": ""
                }
            }
        }   

        like['author']['url'] = data['actor'] + '/'
        like['author']['id'] = data['actor'].split('authors/')[1]
        like['post']['id'] = data['object'].split('posts/')[1]
        like['post']['author']['url'] = target_author_url
        like['post']['author']['id'] = target_author_url.split('authors/')[1]
        return like

