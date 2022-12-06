import json
import urllib.parse

import requests
from rest_framework import status
from rest_framework.response import Response

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from authors.util import AuthorUtil
from common.base_util import BaseUtil
from common.pagination_helper import PaginationHelper
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer
from mysocial.settings import base
from post.serializer import PostSerializer
from remote_nodes.local_default import LocalDefault
from comment.serializers import CommentSerializer
from remote_nodes.node_config_base import NodeConfigBase


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

    post_remote_fields = {
        'id': 'official_id',
        'url': 'url',
        "title": "title",
        "source": "source",
        "origin": "origin",
        "description": "description",
        "contentType": "contentType",
        "image_url": "content",
        "author": "author",
        "categories": "categories",
        "published": "published",
        "visibility": "visibility",
        "unlisted": "unlisted"
    }

    comment_remote_fields = {
        "id": "official_id",
        "type": "type",
        "author": "author",
        "comment": "comment",
        "contentType": "contentType",
        "published": "published",
        "url": "url"
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
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }

    def convert_to_valid_author_url(self, author_id: str) -> str:
        return f'{self.get_base_url()}/authors/{author_id}/'  # watch out for that slash!!!

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
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            response_json = json.loads(response.text)
            author_list = []
            for author_data in response_json:
                data_host = author_data.get('sender_host')
                if data_host is None:
                    continue

                _, host, path, _, _, _ = urllib.parse.urlparse(data_host)
                host = BaseUtil.transform_host(host)
                node_config: NodeConfigBase = base.REMOTE_CONFIG.get(host)
                if node_config is None:
                    print(f"{self}: get_all_followers: Host not found: {host} for {data_host}")
                    continue

                author_url = node_config.convert_to_valid_author_url(author_data['sender_id'])
                author, err = AuthorUtil.from_author_url_to_author(author_url)
                if err is not None:
                    print(f"{self}: get_all_followers: failed to get author via url: {err}")
                    continue

                author_list.append(AuthorSerializer(author).data)

            return author_list
        return []

    def get_remote_follow(self, target: Author, follower: Author) -> Follow:
        """
        Make call to remote node to get a follow object or request

        Returns a Follow object if there is one;
        Returns None if cannot be found
        """
        follower_list = self.get_all_followers(target)
        is_found = False
        for author in follower_list:
            if author.get_url() == follower.get_url():
                is_found = True
                break

        if is_found:
            follow_serializer = FollowRequestSerializer(data={
                'actor': AuthorSerializer(follower).data,
                'object': AuthorSerializer(target).data,
                'hasAccepted': True,
                'localUrl': f'{BaseUtil.get_http_or_https()}{base.CURRENT_DOMAIN}/{Author.URL_PATH}/{target.get_id()}/followers/{follower.get_url()}',
                'id': None
            })
            if not follow_serializer.is_valid():
                for err in follow_serializer.errors:
                    print(f'{self}: get_remote_follow: serialization error: {err}')
                return None
            return follow_serializer.validated_data
        else:
            return None

    def post_local_follow_remote(self, author_actor: Author, author_target: Author) -> dict:
        """Make call to remote node to follow"""
        # friendrequest/from_external/<int:network_id>/<uuid:snd_uuid>/<str:snd_username>/send/<uuid:rec_uuid>/
        snd_uuid = author_actor.get_id()
        snd_username = author_actor.username
        rec_uuid = author_target.get_id()
        url = f'{self.get_base_url()}/friendrequest/from_external/10/{snd_uuid}/{snd_username}/send/{rec_uuid}/'
        response = requests.post(url, headers=self.get_headers())
        if 200 <= response.status_code < 300:
            return {
                'type': 'follow',
                'actor': {'url': author_actor.get_url()},
                'object': {'url': author_target.get_url()},
                'hasAccepted': True,
                'localUrl': f'{BaseUtil.get_http_or_https()}{base.CURRENT_DOMAIN}/{Author.URL_PATH}/{author_target.get_id()}/followers/{author_actor.get_url()}',
                'id': None
            }  # <- GOOD
        print(
            f"{self}: post_local_follow_remote: remote server response: Code ({response.status_code}): {response.text}")
        return response.status_code

    def team12_accept(self, author_actor: Author, author_target: Author):
        """Make call to remote node to accept"""
        # /friendrequest/accept_external/sender/{snd_uuid}/recipient/{rec_uuid}/
        snd_uuid = author_actor.get_id()
        rec_uuid = author_target.get_id()
        url = f'{self.get_base_url()}/friendrequest/accept_external/sender/{snd_uuid}/recipient/{rec_uuid}/'
        response = requests.post(url, headers=self.get_headers())
        if 200 <= response.status_code < 300:
            return

        print(f"{self}: team12_accept: non-successful: ({response.status_code}): {response.text}")
        # silently ignore if it went wrong

    def team12_reject(self, author_actor: Author, author_target: Author):
        """Make call to remote node to reject"""
        # /friendrequest/reject_external/sender/{snd_uuid}/recipient/{rec_uuid}/
        snd_uuid = author_actor.get_id()
        rec_uuid = author_target.get_id()
        url = f'{self.get_base_url()}/friendrequest/reject_external/sender/{snd_uuid}/recipient/{rec_uuid}/'
        response = requests.post(url, headers=self.get_headers())
        if 200 <= response.status_code < 300:
            return

        print(f"{self}: team12_reject: non-successful: ({response.status_code}): {response.text}")
        # silently ignore if it went wrong

    def team12_unfollow(self, author_actor: Author, author_target: Author):
        """Make call to remote node to unfollow"""
        # /{follower_id}/unfollow/{user_id}/
        follower_id = author_actor.get_id()
        user_id = author_target.get_id()
        url = f'{self.get_base_url()}/{follower_id}/unfollow/{user_id}/'
        response = requests.post(url, headers=self.get_headers())
        if 200 <= response.status_code < 300:
            return

        print(f"{self}: team12_unfollow: non-successful: ({response.status_code}): {response.text}")
        # silently ignore if it went wrong

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
        author_url = author_url.rstrip('/')
        author_url = f'{author_url}/'
        response = requests.get(author_url, headers=self.get_headers())

        if response.status_code == 200:
            author_json = json.loads(response.content.decode('utf-8'))
            author_json['url'] = author_url  # since we don't trust their url; this works
            serializer = AuthorSerializer(data=author_json)

            if serializer.is_valid():
                return serializer.validated_data  # <- GOOD RESULT HERE!!!

            print(f'{self} GetAuthorViaUrl: AuthorSerializer: ', serializer.errors)

        return None

    def get_authors_posts(self, request, author_posts_path):
        url = f'{self.get_base_url()}{author_posts_path}'

        try:
            response = requests.get(url, headers=self.get_headers())
            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get author's  post from remote server",
                                status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(f"Failed to get author's post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = []
        post_data = json.loads(response.content.decode('utf-8'))

        for post in post_data:
            data.append(self.convert_team12_post(url, post))

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': 'posts', 'items': data}, status=status.HTTP_200_OK)

    def get_post_by_post_id(self, post_url):
        url = f'{self.get_base_url()}{post_url}'

        try:
            response = requests.get(url, headers=self.get_headers())

            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response(f"Failed to get post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        post_data = json.loads(response.content.decode('utf-8'))

        post = self.convert_team12_post(url, post_data)
        return Response(post, status=status.HTTP_200_OK)

    def get_comments_for_post(self, comments_path, author = None, request = None):
        split_comments = comments_path.split('posts')
        url = f'{self.get_base_url()}{split_comments[0]}{author.display_name}/posts{split_comments[1]}/'
        try:

            response = requests.get(url, headers=self.get_headers())
            if response.status_code < 200 or response.status_code > 300:
                return Response("Failed to get comments for post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response(f"Failed to get comments for post from remote server, error: {e}",
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = []
        comment_data = json.loads(response.content.decode('utf-8'))
        
        for comment in comment_data:
            data.append(self.convert_team12_comment(url, comment))
        
        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'type': 'posts', 'items': data}, status=status.HTTP_200_OK)

    def create_comment_on_post(self, comments_path, data, extra_data = None):
        split_comments = comments_path.split('posts')
        display_name = extra_data['displayName']

        url = f'{self.get_base_url()}{split_comments[0]}{display_name}/posts{split_comments[1]}/'
        data = self.create_team12_comment(data)
        response = requests.post(url = url, data = json.dumps(data), headers=self.get_headers())
        
        if response.status_code < 200 or response.status_code > 300:
            return Response(
                f"Failed to get post from remote server, error {json.loads(response.content)}",
                status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("Successfully created comment to team 12!", status=status.HTTP_200_OK)
        
    
    def convert_team12_post(self, url, post):
        post["url"] = url

        serializer = PostSerializer(data=post)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors
    
    def convert_team12_comment(self, url, comment):
        comment["url"] = url

        serializer = CommentSerializer(data = comment)
        if serializer.is_valid():
            return serializer.data
        else:
            return serializer.errors
    
    def create_team12_comment(self, data):
        comment = {
            "comment": data['comment']
        }
        return comment