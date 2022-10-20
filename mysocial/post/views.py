from venv import create
from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializer import PostSerializer, CreatePostSerializer
from authors.models import Author
from .models import Post, Visibility
from rest_framework import status
import logging, uuid

logger = logging.getLogger("mylogger")

class PostView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CreatePostSerializer
        else:
            return PostSerializer
    
    def get_queryset(self):
        return Post.objects.all()
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk = self.kwargs['post_id'])
        return obj

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            post = Post.objects.get(official_id=kwargs['post_id'])

            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
    
    def delete(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            if self.authorize_user(kwargs['author_id']) == False:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            
            post = Post.objects.get(official_id=kwargs['post_id'])
            post.delete()

            serializer = PostSerializer(post)
            return Response(serializer.data)

        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
    
    # update the post whose id is post_id
    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            serializer = CreatePostSerializer(instance = self.get_object(), data=request.data, partial = True)
            if serializer.is_valid():
                post = serializer.save()
                return Response(PostSerializer(post).data, status = status.HTTP_200_OK)
            
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()

    # update or create post whose id is post_id
    def put(self, request: Request, *args, **kwargs) -> HttpResponse:
        if self.authorize_user(kwargs['author_id']) == False:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        instance = self.get_object_or_none()
        if instance == None:
            return self.create_post(request, **kwargs)
        else:
            return self.post(request, *args, **kwargs)

    def create_post(self, request, **kwargs):
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data['official_id'] = kwargs['post_id']
            data['author'] = Author.objects.get(official_id = kwargs['author_id'])
            post = serializer.create(validated_data=data)
            return Response(PostSerializer(post).data, status = status.HTTP_200_OK)
        else:
            return HttpResponseNotFound()

    def authorize_user(self, post_author_id):
        return post_author_id == self.request.user.official_id

    def get_object_or_none(self):
        try: 
            return self.get_object()
        except:
            return None


class PublicPostView(GenericAPIView):
    def get_queryset(self):
        return Post.objects.all()

    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            public_posts = Post.objects.filter(
                visibility = Visibility.PUBLIC
            )

            serializer = PostSerializer(public_posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
class CreationPostView(GenericAPIView):
    serializer_class = CreatePostSerializer

    def post(self, request, *args, **kwargs):
        logger.info("PLEASE")
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                data['author'] = Author.objects.get(official_id = kwargs['author_id'])
                post = serializer.create(validated_data=data)
                return Response(PostSerializer(post).data, status = status.HTTP_200_OK)
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
