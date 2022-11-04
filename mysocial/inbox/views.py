from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpRequest, QueryDict
import logging
import json
import ast

# models
from .models import Inbox
from authors.models import Author
from likes.models import Like
from post.models import Post
from comment.models import Comment
from follow.models import Follow

# serializing
from rest_framework import serializers
from .inbox_serializers import InboxSerializer, CreateInboxSerializer, CreatePOSTObjectSerializer
from authors.serializers.author_serializer import AuthorSerializer
from post.serializer import PostSerializer
from likes.views import LikesSerializer, CreateLikeSerializer
from follow.serializers.follow_serializer import FollowRequestSerializer
from comment.serializers import CommentSerializer, CreateCommentSerializer

logger = logging.getLogger("mylogger")

# like_object_url = like_data[objectURL]
# author_uuid = like_object_url.split('authors/')[1].split('/posts')[0]

# URI: service/authors/<uuid:author_id>/inbox
# handles POST, GET, DELETE
# objects: likes, follows, posts, comments
class InboxView(GenericAPIView):
    def get_serializer_class(self):
        # POST can be like, follow, comment, or post object
        if self.request.method == 'POST':
            return CreatePOSTObjectSerializer

        # GET returns inbox objects only
        elif self.request.method == 'GET':
            return CreateInboxSerializer

        else:
            print('serializer error: ' + __str__)
            # maybe log it
            return

    def get_queryset(self):
        return Inbox.objects.all()

    def __handle_likes(self, request):
        try:
            print('Creating Like Object...')
            #request = json.dumps(request)
            print(type(request))
            print(request)
            serializer = CreateLikeSerializer(data=request)
            print(serializer)
            
            if serializer.is_valid():
                print('valid data...')
                like_data = serializer.data
                print(like_data)
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

    def __handle_follows(self, request):
        return

    def __handle_posts(self, request):
        print('IN POSTS')
        return

    def __handle_comments(self, request):
        print('IN COMMENTS')
        serializer = CreateCommentSerializer(data=request.body.decode('utf-8'))
        print('serializer:')
        print(serializer)

        if serializer.is_valid():
            data = serializer.data
            print (data)
            return Response(CommentSerializer(comment).data)

        else:
            return HttpResponseNotFound

    # POST: either a like, follow, post, or comment; follows need approval
    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        print(f'REQ:\n{request}\nARGS:\n{args}\nKWARGS:\n{kwargs}')
        mail_type = request.data['type']

        # print('')
        # decoded_data = request.body.decode('utf-8')
        # decoded_data = 'r"""' + decoded_data + '"""'
        # print('Req data:\n' + decoded_data)
        # print(type(decoded_data))

        # new1 = json.loads(decoded_data)
        # print(new1)
        # data_dict = ast.literal_eval(decoded_data)
        # print(type(data_dict))
        # print(data_dict)
        # data = request.data
        # dict_str = dict_str.replace(" ", "")
        # item_dict = json.loads(dict_str)
        # print('new dict_str\n' + str(item_dict))

        if mail_type.upper() == 'LIKE':
            return self.__handle_likes(request=request)
        elif mail_type.upper() == 'FOLLOW':
            return self.__handle_follows(request)
        elif mail_type.upper() == 'POST':
            return self.__handle_posts(request)
        elif mail_type.upper() == 'COMMENT':
            return self.__handle_comments(request)
        else:
            print('XD')
            return HttpResponseNotFound

    # GET: list of items sent to author_id
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        print('HTTP REQUEST: \n' + str(HttpRequest) + 'REQUEST DATA:\n' + str(request.data))
        try:
            #TODO
            return Response({'HTTP GET RESPONSE': 'will send inbox data after implementing POST likes'}, status = status.HTTP_200_OK)

        except Exception as e:
            print('error:\n' + str(e))
            logger.info(e)
            return HttpResponseNotFound

    #TODO
    # DELETE: clears inbox
    def delete(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:

            if serializer.is_valid():

                return Response(ser.data)
            else:
                return HttpResponseBadRequest

        except Exception as e:
            print('\nerror:\n' + str(e))
            logger.info(e)
            return HttpResponseNotFound
