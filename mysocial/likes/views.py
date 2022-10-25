from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from .models import Like
from authors.models import Author
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import serializers
from post.serializer import PostSerializer 
from authors.serializers.author_serializer import AuthorSerializer

'''
    context = models.CharField(max_length=400)
    summary = models.CharField(max_length=400)
    type = 'like'  # requirements spelled with capital l
    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)
    object = models.ForeignKey('post.Post', on_delete = models.CASCADE)
'''
class LikesSerializer(serializers.ModelSerializer):
    context = serializers.CharField()
    summary = serializers.CharField()
    type = serializers.CharField()
    author = serializers.SerializerMethodField()
    object = serializers.CharField()

    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author

    class Meta:
        model = Like
        #fields = ['context', 'summary', 'type', 'author', 'object']
        fields = '__all__'

# ---------------VIEWS-----------------------------------------------
class LikedView(GenericAPIView):
    def get_queryset(self):
        return Like.objects.all()

    def get(self, request: Request, *args, **kwargs):
        try:
            author = Author.objects.get(official_id=kwargs['author_id'])
            liked_posts = Like.objects.filter(author=author)
            ser = LikesSerializer(liked_posts, True)
            return Response({'type':'liked', 'items':ser.data})

        except Exception as e:
            print(e)
            return HttpResponseNotFound

class PostLikesView(GenericAPIView):
    def get():
        return HttpResponseForbidden

class CommentLikesView(GenericAPIView):
    def get():
        return HttpResponseForbidden






