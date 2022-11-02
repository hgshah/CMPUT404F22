from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpRequest
import logging

# models
from .models import Inbox
from authors.models import Author
from likes.models import Like
from post.models import Post
from comment.models import Comment
from follow.models import Follow

# serializing
from rest_framework import serializers
from . import inbox_serializers
from authors.serializers.author_serializer import AuthorSerializer
from post.serializer import PostSerializer
from likes.views import LikesSerializer, CreateLikeSerializer
from follow.serializers.follow_serializer import FollowRequestSerializer
from comment.serializers import CommentSerializer, CreateCommentSerializer

logger = logging.getLogger("mylogger")


# def handle_inbox_likes(request, args, kwargs) -> HttpResponse:
# def handle_inbox_follows(request, args, kwargs):
# def handle_inbox_posts(request, args, kwargs):
#     #TODO
#     return HttpResponseForbidden
# def handle_inbox_comments(request, args, kwargs):
#     #TODO
#     return HttpResponseForbidden

# service/authors/<uuid:author_id>/inbox
# handles POST, GET
# objects: likes, follows, posts, comments
class InboxView(GenericAPIView):
    def get_serializer_class(self):
        # POST can be like, follow, comment, or post object
        if self.request.method == 'POST':
            return CreateLikeSerializer
        # GET returns inbox objects only
        elif self.request.method == 'GET':
            return CommentSerializer
        else:
            print('serializer error' + __str__)
            return

    def get_queryset(self):
        # may be diff for POST and GET later on
        return Inbox.objects.all()

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        print('HTTP REQUEST: \n' + str(HttpRequest) + 'REQUEST DATA:\n' + str(request.data))
        try:
            #TODO
            return Response({'HTTP GET RESPONSE': 'will send inbox data after implementing POST likes'}, status = status.HTTP_200_OK)

        except Exception as e:
            print('error:\n' + str(e))
            logger.info(e)
            return HttpResponseNotFound

    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        print(f'REQ:\n{request}\nARGS:\n{args}\nKWARGS:\n{kwargs}')

        try:
            serializer = CreateLikeSerializer(data=request.data)
            print('Creating Like Object')

            if serializer.is_valid():
                like_data = serializer.data
                # like_object_url = like_data[objectURL]
                # author_uuid = like_object_url.split('authors/')[1].split('/posts')[0]
                like_data['author'] = Author.objects.get(official_id=like_data['author'])
                like_obj = serializer.create(data=like_data)
                ser = LikesSerializer(like_obj)
                return Response(ser.data)
            else:
                return HttpResponseBadRequest

        except Exception as e:
            print('\nerror:\n' + str(e))
            logger.info(e)
            return HttpResponseNotFound
