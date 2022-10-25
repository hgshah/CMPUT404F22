from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request

# models needed
from .models import Like
from authors.models import Author
from post.models import Post
#need to import comments for likes

# serializing
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

# --------------- VIEWS ---------------
# for URL: ://service/authors/{AUTHOR_ID}/inbox/
class InboxView(GenericAPIView):
    def post(self, request: Request, *args, **kwargs):
        #TODO
        return HttpResponseForbidden

# for URL: ://service/authors/{AUTHOR_ID}/liked
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
    def get(self, request: Request, *args, **kwargs):
        try:
            post = Post.objects.get(official_id=kwargs['post_id'])
            post_likes = Like.objects.filter(object=request.get_full_path()[:-5])
            ser = LikesSerializer(post_likes, True)
            return Response(ser)

        except Exception as e:
            print(e)
            return HttpResponseNotFound

#TODO
class CommentLikesView(GenericAPIView):
    def get(self, request: Request, *args, **kwargs):
        try:

            return Response()

        except Exception as e:
            print(e)
            return HttpResponseForbidden
