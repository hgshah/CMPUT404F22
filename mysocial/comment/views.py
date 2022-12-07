
from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from authors.models.author import Author
from comment.serializers import CommentSerializer, CreateCommentSerializer, CommentSerializerList
from authors.util import AuthorUtil
from authors.serializers.author_serializer import AuthorSerializer
from .models import Comment
from post.models import Post
from rest_framework import status
import logging

from common.pagination_helper import PaginationHelper
from mysocial.settings import base
from remote_nodes.remote_util import RemoteUtil
import json

logger = logging.getLogger("mylogger")
class CommentView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        else:
            return CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

    @extend_schema(
        responses=CommentSerializerList,
        summary="comment_get_comments_on_post",
        tags=["comment", RemoteUtil.REMOTE_IMPLEMENTED_TAG, RemoteUtil.TEAM7_CONNECTED, RemoteUtil.TEAM12_CONNECTED, RemoteUtil.TEAM14_CONNECTED]
    )
    @action(detail=True, methods=['get'], url_name='comment_get_comments_on_post')
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        '''
        Get a paginated list of comments for a post
        '''
        node: Author = request.user
        if not node.is_authenticated:
            return HttpResponseNotFound()

        if node.is_authenticated_user:
            try:
                target_author = Author.get_author(kwargs['author_id'])
            except:
                return Response(f"Error getting author id: {kwargs['author_id']}", status.HTTP_400_BAD_REQUEST)

            #local -> local
            if target_author.is_local():
                try:
                    post = Post.objects.get(official_id=kwargs['post_id'])
                    comments = Comment.objects.filter(post = post)
                    serializer = CommentSerializer(comments, many = True)
                    data = serializer.data
                    data, err = PaginationHelper.paginate_serialized_data(request, data)

                    if err is not None:
                        return Response(f'{err}', status = status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'type': 'comments', 'items': data})

                except Exception as e:
                    logger.info(e)
                    return HttpResponseNotFound

            # local -> remote
            else:
                node_config = base.REMOTE_CONFIG.get(target_author.host)
                return node_config.get_comments_for_post(request.get_full_path(), author = target_author, request = request)

        # remote -> local
        if request.user.is_authenticated_node:
            try:
                post = Post.objects.get(official_id=kwargs['post_id'])
                comments = Comment.objects.filter(post = post)
                serializer = CommentSerializer(comments, many = True)
                data = serializer.data
                data, err = PaginationHelper.paginate_serialized_data(request, data)

                if err is not None:
                    return Response(f'{err}', status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'type': 'comments', 'items': data})

            except Exception as e:
                logger.info(e)
                return HttpResponseNotFound

    @extend_schema(
            summary = "comment_create_comment",
            request = CreateCommentSerializer,
            
            responses = CommentSerializer,
            tags=['comment', RemoteUtil.REMOTE_IMPLEMENTED_TAG, RemoteUtil.TEAM7_CONNECTED, RemoteUtil.TEAM12_CONNECTED, RemoteUtil.TEAM14_CONNECTED]
        )
    @action(detail=True, methods=['get'], url_name='comment_post')
    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        User story: As an author, I want to comment on posts that I can access
        """

        node: Author = request.user
        if not node.is_authenticated:
            return HttpResponseNotFound()

        if node.is_authenticated_user:
            try:
                post_author = Author.get_author(kwargs['author_id'])
            except:
                return Response(f"Error getting author id: {kwargs['author_id']}", status.HTTP_400_BAD_REQUEST)

            #local -> local
            if post_author.is_local():
                try:
                    post = Post.objects.get(official_id = kwargs['post_id'])
                except:
                    return Response(f'Failed to get post for post id: {kwargs["post_id"]}', status = status.HTTP_400_BAD_REQUEST)
                
                serializer = CreateCommentSerializer(data=request.data)
                
                if serializer.is_valid() == False:
                    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
                else:
                    data = serializer.data
                    comment = self.create_comment(json_author = AuthorSerializer(node).data, comment = request.data['comment'], contentType = request.data['contentType'], post = post)
                    return Response(comment, status = status.HTTP_200_OK)

            # local -> remote
            else:
                node_config = base.REMOTE_CONFIG.get(post_author.host)
                data = request.data
        
                try:
                    requesting_author_id = self.request.user.get_id()
                    requesting_author = Author.get_author(requesting_author_id)
                    json_author = AuthorSerializer(requesting_author).data 
                except:
                    return Response(f"Could not get local author {requesting_author_id}", status = status.HTTP_400_BAD_REQUEST)

                data['actor'] =  json_author["url"]

                # get the post id,kwargs
                # get the original author id kwargs
                # get the author url, post_author
                try:
                    post = {
                        "post": {
                            "post": {
                            "id": str(kwargs['post_id']),
                            "author" : {
                                "id": str(kwargs['author_id']),
                                "url": post_author.get_url()
                            }
                            }
                        },
                        "displayName": post_author.display_name
                    }
                except Exception as e:
                    return Response(f'Cannot form extra data {e}', status = status.HTTP_400_BAD_REQUEST)

                return node_config.create_comment_on_post(request.get_full_path(), data = data, extra_data = post)

        # remote -> local
        if request.user.is_authenticated_node:
            try:
                post = Post.objects.get(official_id = kwargs['post_id'])
            except:
                return Response(f'Failed to get post for post id: {kwargs["post_id"]}', status = status.HTTP_400_BAD_REQUEST)

            try:
                requesting_author_url = request.data['actor'] 
                requesting_author = AuthorUtil.from_author_url_to_author(requesting_author_url)[0] 
                json_author = AuthorSerializer(requesting_author).data 
            except:
                return Response(f"Could not get remote requesting author from url: {request.data['actor']}", status = status.HTTP_400_BAD_REQUEST)

            comment = self.create_comment(json_author = json_author, comment = request.data['comment'], contentType = request.data['contentType'], post = post)
            return Response(comment, status = status.HTTP_200_OK)

    def create_comment(self, json_author, contentType, comment, post):
        comment = Comment.objects.create(author = json_author, comment = comment, contentType = contentType, post = post)
        return CommentSerializer(comment).data
