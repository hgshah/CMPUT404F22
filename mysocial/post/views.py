from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializer import PostSerializer, CreatePostSerializer
from django.core.paginator import Paginator
from authors.models import Author
from .models import Post, Visibility
from rest_framework import status
import logging, json
from urllib.request import urlopen
from common import PaginationHelper

logger = logging.getLogger("mylogger")

class PostView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CreatePostSerializer
        else:
            return PostSerializer
    
    def get_queryset(self):
        return Post.objects.all()
    
    #munsu, October 19, https://stackoverflow.com/questions/43859053/
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk = self.kwargs['post_id'])
        return obj

    # Get specific post by post id
    # GET /authors/{AUTHOR_UUID}/posts/{POST_UUID}
    #Peter, October 19, https://stackoverflow.com/questions/1496346/passing-a-list-of-kwargs
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            post = Post.objects.get(official_id=kwargs['post_id'])
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
    
    # DELETE /authors/{AUTHOR_UUID}/posts/{POST_UUID}
    # Wolph, October 19, https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
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
    #awwester, October 19, https://stackoverflow.com/questions/31173324/django-rest-framework-update-field
    #Ameya Joshi, October 19, https://stackoverflow.com/questions/62381855/how-to-update-model-objects-only-one-field-data-when-doing-serializer-save
    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            if self.authorize_user(kwargs['author_id']) == False:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            serializer = CreatePostSerializer(instance = self.get_object(), data=request.data, partial = True)
            if serializer.is_valid():
                post = serializer.save()

                return Response(PostSerializer(post).data, status = status.HTTP_200_OK)
            
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()

    # update or create post whose id is post_id
    #Daniel van Flymen, October 19, https://stackoverflow.com/questions/35024781/create-or-update-with-put-in-django-rest-framework
    def put(self, request: Request, *args, **kwargs) -> HttpResponse:
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

    #k44, October 19, https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django 
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

    # get all public posts
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

# /authors/{AUTHOR_ID}/posts/
class CreationPostView(GenericAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return CreatePostSerializer
        else:
            return PostSerializer

    def get_queryset(self):
        return Post.objects.all()
    
    # get posts by the author
    def get(self, request, *args, **kwargs):
        author = Author.objects.get(official_id = kwargs['author_id'])
        posts = Post.objects.filter(author = author).order_by('-published')
        serializer = PostSerializer(posts, many = True)
        data = serializer.data
        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            return HttpResponseNotFound()
        else:
            return Response({'type': 'posts', 'items': data})

    # create brand new post, no id
    # Édouard Lopez, October 19, https://stackoverflow.com/questions/5255913/kwargs-in-django
    def post(self, request, *args, **kwargs):
        try:
            serializer = CreatePostSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                data['author'] = Author.objects.get(official_id = kwargs['author_id'])
                post = serializer.create(validated_data=data)
                return Response(PostSerializer(post).data, status = status.HTTP_200_OK)
        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()

