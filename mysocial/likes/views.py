from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpRequest
import logging

# models
from .models import Like, Inbox
from authors.models import Author
from post.models import Post
from comment.models import Comment

# serializing
from rest_framework import serializers
from post.serializer import PostSerializer 
from authors.serializers.author_serializer import AuthorSerializer
from follow.serializers.follow_serializer import FollowRequestSerializer
from comment.serializers import CommentSerializer, CreateCommentSerializer

logger = logging.getLogger("mylogger")

#                                                                             #
#-------------------------------- SERIALIZERS --------------------------------#
#                                                                             #
class LikesSerializer(serializers.ModelSerializer):
    context = serializers.CharField()
    summary = serializers.CharField()
    type = serializers.CharField()
    author = serializers.SerializerMethodField()
    objectURL = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author

    def get_objectURL(self, obj):
        item = PostSerializer(obj.objectURL).data['id']
        return item

    class Meta:
        model = Like
        fields = ['context', 'summary', 'type', 'author', 'objectURL']
        #fields = '__all__'

class CreateLikeSerializer(serializers.ModelSerializer):
    def create(self, data):
        like = Like.objects.create(**data)
        return like

    class Meta:
        model = Like
        fields = ['context', 'summary', 'type', 'author', 'objectURL', 'objectType']

#TODO later
# class InboxSerializer(serializers.ModelSerializer):
#     type = serializers.CharField()
#     author = serializers.CharField()
#     content = serializers.CharField()

#     class Meta:
#         model = Inbox
#         fields = ['type', 'author', 'content']


#                                                                             #
#----------------------------------- VIEWS -----------------------------------#
#                                                                             #
# for URL: ://service/authors/{AUTHOR_ID}/inbox/
def handle_inbox_likes(request, args, kwargs) -> HttpResponse:
    try:
        serializer = CreateLikeSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            like = serializer.create(validated_data=data)

            return Response(LikesSerializer(like).data)
        else:
            return("error")

    except Exception as e:
        print(e)
        return HttpResponseNotFound

# def handle_inbox_follows(request, args, kwargs):

# def handle_inbox_posts(request, args, kwargs):
#     #TODO
#     return HttpResponseForbidden

# def handle_inbox_comments(request, args, kwargs):
#     #TODO
#     return HttpResponseForbidden

# source/authors/<uuid:author_id>/inbox
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
        print(f'REQ\n {request} \nARGS\n {args} \nKWARGS\n {kwargs}')

        try:
            serializer = CreateLikeSerializer(data=request.data)

            if serializer.is_valid():
                like_data = serializer.data
                like_data['author'] = Author.objects.get(official_id=kwargs['author_id'])
                like_data['objectURL'] = Post.objects.get(official_id=like_data['objectURL'])
                like_obj = serializer.create(data=like_data)
                ser = LikesSerializer(like_obj)
                return Response(ser.data)

        except Exception as e:
            print('error:\n' + str(e))
            logger.info(e)
            return HttpResponseNotFound

# source/authors/<uuid:author_id>/liked
class LikedView(GenericAPIView):
    def get_queryset(self):
        return Like.objects.all()

    def get(self, request: Request, *args, **kwargs):
        try:
            author = Author.objects.get(official_id=kwargs['author_id'])
            liked_posts = Like.objects.filter(author=author)
            ser = LikesSerializer(liked_posts, many=True)
            return Response({'type':'liked', 'items':ser.data})

        except Exception as e:
            print(e)
            return HttpResponseNotFound

# source/authors/<uuid:author_id>/posts/<uuid:post_id>/likes
class PostLikesView(GenericAPIView):
    def get_queryset(self):
        return Like.objects.all()

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            post = Post.objects.get(official_id=kwargs['post_id'])
            post_likes = Like.objects.filter(objectURL=post.official_id)
            ser = LikesSerializer(post_likes, many=True)
            return Response(ser.data)

        except Exception as e:
            print('Error:\n' + e)
            return HttpResponseNotFound

# source/authors/<uuid:author_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>/likes
class CommentLikesView(GenericAPIView):
    def get_queryset(self):
        return Like.objects.all()

    def get(self, request: Request, *args, **kwargs):
        try:
            comment = Comment.objects.get(official_id=kwargs['comment_id'])
            comment_likes = Like.objects.filter(objectURL=comment.official_id)
            ser = LikesSerializer(comment_likes, many=True)
            return Response(ser.data)

        except Exception as e:
            print('Error:\n' + e)
            return HttpResponseNotFound
