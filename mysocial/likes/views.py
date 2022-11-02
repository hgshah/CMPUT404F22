from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpRequest
import logging

# models
from .models import Like
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
'''
class Like(models.Model):
    context = models.CharField(max_length=400)
    summary = models.CharField(max_length=400)
    type = 'like'
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    objectURL = models.UUIDField(primary_key=False, default=0, editable=True)

    official_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_received = models.DateTimeField(default=timezone.now)
    object_type = models.CharField(choices=LikedItem.choices, default=LikedItem.POST, max_length=16, blank=False)
    ref_post = models.ForeignKey('post.Post', on_delete=models.CASCADE, blank=True, null=True)
    ref_comment = models.ForeignKey('comment.Comment', on_delete=models.CASCADE, blank=True, null=True)
'''
class LikesSerializer(serializers.ModelSerializer):
    context = serializers.CharField()
    summary = serializers.CharField()
    type = serializers.CharField()
    author = serializers.SerializerMethodField()
    objectURL = serializers.CharField()

    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author

    # def get_objectURL(self, obj):
    #     item = PostSerializer(obj.objectURL).data['id']
    #     return item

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
        fields = ['context', 'summary', 'type', 'author', 'objectURL', 'object_type']

#                                                                             #
#----------------------------------- VIEWS -----------------------------------#
#                                                                             #

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
