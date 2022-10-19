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
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
        serializer = PostSerializer(public_posts, many=True)
        return Response(serializer.data)

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
