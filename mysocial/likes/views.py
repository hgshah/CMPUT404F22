from django.shortcuts import render

from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.decorators import action
from rest_framework import status

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from authors.models.author import Author
from likes.models import Like
from likes.serializers import LikeSerializer, LikeSerializerList

from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.decorators import action
from rest_framework import serializers

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from remote_nodes.remote_util import RemoteUtil
from likes.models import Like, LikeType
from mysocial.settings import base
import json
# Create your views here.
class LikeView(GenericViewSet):
    '''
        Response will be a list of authors!! 
    '''

    @extend_schema(
        responses=AuthorSerializer,
        summary="likes_retrieve_authors_for_post",
        tags=["likes", RemoteUtil.REMOTE_IMPLEMENTED_TAG, RemoteUtil.TEAM12_CONNECTED, RemoteUtil.TEAM14_CONNECTED]
    )
    @action(detail=True, methods=['get'], url_name='get_authors_liked_on_post')
    def get_authors_liked_on_post(self, request: Request, *args, **kwargs) -> HttpResponse:
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
                authors = self.get_authors_for_local_like(request, LikeType.POST) 
                return Response(authors, status = status.HTTP_200_OK)

            # local -> remote
            else:
                object_id = request.path
                node_config = base.REMOTE_CONFIG.get(target_author.host)
                return node_config.get_authors_liked_on_post(object_id)

        # remote -> local
        if request.user.is_authenticated_node:
            authors = self.get_authors_for_local_like(request, LikeType.POST) 
            return Response(authors, status = status.HTTP_200_OK)
    
    @extend_schema(
        responses=AuthorSerializer(),
        summary="likes_retrieve_authors_liked_on_comment",
        tags=["likes", RemoteUtil.REMOTE_IMPLEMENTED_TAG]
    )
    @action(detail=False, pagination_class = None, methods=['get'], url_name='get_authors_liked_on_comment')
    def get_authors_liked_on_comment(self, request: Request, *args, **kwargs) -> HttpResponse:
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
                authors = self.get_authors_for_local_like(request, LikeType.COMMENT) 
                return Response(authors, status = status.HTTP_200_OK)

            # local -> remote
            else:
                object_id = request.path
                node_config = base.REMOTE_CONFIG.get(target_author.host)
                response = node_config.get_authors_liked_on_comment(object_id)
                if response.status_code < 200 or response.status_code > 300:
                    return Response("Failed to get author likes for post on remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response(json.loads(response.content), status = status.HTTP_200_OK)

        # remote -> local
        if request.user.is_authenticated_node:
            authors = self.get_authors_for_local_like(request, LikeType.COMMENT) 
            return Response(authors, status = status.HTTP_200_OK)
            
    @extend_schema(
        responses=LikeSerializerList,
        summary="like_get_author_likes",
        tags=["likes", RemoteUtil.REMOTE_IMPLEMENTED_TAG]
    )
    @action(detail=True, methods=['get'], url_name='get_authors_likes')
    def get_author_liked(self, request, *args, **kwargs) -> HttpResponse:
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
                author_likes = Like.objects.filter(author_id = target_author.get_id())
                return Response({
                    'type': 'liked',
                    'items': LikeSerializer(author_likes, many = True).data
                }, status = status.HTTP_200_OK)

            # local -> remote
            else:
                node_config = base.REMOTE_CONFIG.get(target_author.host)
                response = node_config.get_authors_likes(target_author.get_url())

                if response.status_code < 200 or response.status_code > 300:
                    return Response("Failed to get all author likes on remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response(json.loads(response.content), status = status.HTTP_200_OK)

        # remote -> local
        if request.user.is_authenticated_node:
            author_likes = Like.objects.filter(author_id = kwargs['author_id'])
            return Response({
                'type': 'liked',
                'items': LikeSerializer(author_likes, many = True).data
            }, status = status.HTTP_200_OK)
    
    def get_authors_for_local_like(self, request, object_type):
        object_id = request.path.split('/likes')[0]
        return Like.objects.filter(object__contains = object_id, object_type = object_type).values_list('author', flat = True)
    
