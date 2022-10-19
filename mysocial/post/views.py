from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework.request import Request
from .serializer import PostSerializer
from rest_framework.generics import GenericAPIView
from .serializer import PostSerializer, CreatePostSerializer
from authors.models import Author
from .models import Post, Visibility
from rest_framework import status
import logging
logger = logging.getLogger("mylogger")
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

class PostView(GenericAPIView):
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
            # check if logged in users id == authors id on about to delete post
            post_author_id = Author.objects.get(official_id = kwargs['author_id']).official_id
            if post_author_id != self.request.user.official_id:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

            post = Post.objects.get(official_id=kwargs['post_id'])
            post.delete()

            serializer = PostSerializer(post)
            return Response(serializer.data)

        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()

class CreationPostView(GenericAPIView):
    serializer_class = CreatePostSerializer

    def post(self, request, *args, **kwargs):
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
