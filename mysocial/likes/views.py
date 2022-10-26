from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

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
    object = models.CharField(max_length=400)
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

class CreateLikeSerializer(serializers.ModelSerializer):
    def create(self, data):
        like = Like.objects.create(**data)
        return like

#                                                                             #
#----------------------------------- VIEWS -----------------------------------#
#                                                                             #

# for URL: ://service/authors/{AUTHOR_ID}/inbox/
def handle_inbox_likes(request, args, kwargs):
    try:
        ser = CreateLikeSerializer(data=request.data)

        if ser.is_valid():
            return Response(ser.validated_data, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return HttpResponseNotFound

def handle_inbox_follows(request, args, kwargs):
    #TODO
    return HttpResponseForbidden

def handle_inbox_posts(request, args, kwargs):
    #TODO
    return HttpResponseForbidden

def handle_inbox_comments(request, args, kwargs):
    #TODO
    return HttpResponseForbidden

class InboxView(GenericAPIView):
    def post(self, request: Request, *args, **kwargs):
        if kwargs['type'] == 'like':
            handle_inbox_likes(request, args, kwargs)        
        elif kwargs['type'] == 'follow':
            handle_inbox_follows(request, args, kwargs)            
        elif kwargs['type'] == 'post':
            handle_inbox_posts(request, args, kwargs)
        elif kwargs['type'] == 'comment':
            handle_inbox_comments(request, args, kwargs)
        else:
            return HttpResponseBadRequest

    def get(self, request: Request, *args, **kwargs):
        #TODO
        return       

# for URL: ://service/authors/{AUTHOR_ID}/liked
class LikedView(GenericAPIView):
    # def get_queryset(self):
    #     return Like.objects.all()
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
            return Response(ser.data)

        except Exception as e:
            print(e)
            return HttpResponseNotFound

#TODO need comments
class CommentLikesView(GenericAPIView):
    def get(self, request: Request, *args, **kwargs):
        try:

            return Response()

        except Exception as e:
            print(e)
            return HttpResponseForbidden
