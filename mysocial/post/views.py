from django.http.response import HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializer import PostSerializer
from rest_framework.generics import GenericAPIView
from .serializer import PostSerializer, CreatePostSerializer
from authors.models import Author
from rest_framework import status
import logging
logger = logging.getLogger("mylogger")

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
