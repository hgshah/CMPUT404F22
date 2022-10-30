from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

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

# service/authors/<uuid:author_id>/inbox
class InboxView(GenericAPIView):
    def post(self, request: Request, *args, **kwargs):
        print(f'INFO\n {request} \nARGS\n {args} \nKWARGS\n {kwargs}')
        authorUUID = kwargs['author_id']
        return handle_inbox_likes(request, args, kwargs)

    # everything in inbox (likes, follows, posts, comments)
    def get(self, request: Request, *args, **kwargs):
        #TODO
        #should get by author id, sort by date decending
        return       

# for URL: ://service/authors/{AUTHOR_ID}/liked
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
            post_likes = Like.objects.filter()
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
            comment_likes = Like.objects.filter()
            ser = LikesSerializer(comment_likes, many=True)
            return Response(ser.data)

        except Exception as e:
            print('Error:\n' + e)
            return HttpResponseNotFound
