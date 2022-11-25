
from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from authors.models.author import Author
from comment.serializers import CommentSerializer, CreateCommentSerializer, CommentSerializerList
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
        tags=["comment", RemoteUtil.REMOTE_IMPLEMENTED_TAG]
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
                response = node_config.get_comments_for_post(request.get_full_path())
                if response.status_code < 200 or response.status_code > 200:
                    return Response("Failed to get post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response(json.loads(response.content), status = status.HTTP_200_OK)

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
            tags=['comment']
        )
    @action(detail=True, methods=['get'], url_name='comment_post')
    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        User story: As an author, I want to comment on posts that I can access
        """
        try:
            author = Author.get_author(self.request.user.get_id())
        except:
            return Response(f'Failed to get author. Are you logged in? Did you pass auth information?', status = status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(official_id = kwargs['post_id'])
        except:
            return Response(f'Failed to get post for post id: {kwargs["post_id"]}', status = status.HTTP_400_BAD_REQUEST)
        
        serializer = CreateCommentSerializer(data=request.data)
        
        if serializer.is_valid() == False:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            data['author'] = author
            data['post'] = post
            comment = serializer.create(validated_data = data)
            return Response(CommentSerializer(comment).data, status = status.HTTP_200_OK)
