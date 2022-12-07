from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializer import PostSerializer, CreatePostSerializer, SharePostSerializer, PostSerializerList
from rest_framework import serializers
from authors.models.author import Author
from .models import Post, Visibility
from rest_framework import status
import logging
from common.pagination_helper import PaginationHelper
from follow.follow_util import FollowUtil
from inbox.models import Inbox
from mysocial.settings import base
from remote_nodes.remote_util import RemoteUtil
import json
from common.post_helper import PostHelper
import base64
from post.custom_renderers import JPEGRenderer, PNGRenderer

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
    #Peter, October 19, https://stackoverflow.com/questions/1496346/passing-a-list-of-
    @extend_schema(
        summary = "post_get_post_by_id",
        responses = PostSerializer,
        tags=['post', RemoteUtil.REMOTE_IMPLEMENTED_TAG, RemoteUtil.TEAM12_CONNECTED, RemoteUtil.TEAM14_CONNECTED]
    )
    @action(detail=True, methods=['get'], url_name='post_get_post_by_id')
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        Get specific post by post id
        """
        node: Author = request.user
        if not node.is_authenticated:
            return HttpResponseNotFound()
        
        if node.is_authenticated_user:
            try:
                target_author = Author.get_author(kwargs['author_id'])
            except:
                return Response(f"Error getting author id: {kwargs['author_id']}", status.HTTP_400_BAD_REQUEST)

            #local -> local
            if target_author.is_local():
                try:
                    post = Post.objects.get(official_id=kwargs['post_id'])
                    post_with_comments = PostHelper.add_comments_and_count(author = target_author, post = post)
               
                    return Response(post_with_comments)
                except Exception as e:
                    logger.info(e)
                    return HttpResponseNotFound()

            # local -> remote
            else:
                node_config = base.REMOTE_CONFIG.get(target_author.host) 
                return node_config.get_post_by_post_id(request.path)

        # remote -> local
        if request.user.is_authenticated_node:
            try:
                post = Post.objects.get(official_id=kwargs['post_id'])
                target_author = Author.get_author(kwargs['author_id'])
                
                post_with_comments = PostHelper.add_comments_and_count(author = target_author, post = post)
                return Response(post_with_comments)
            except Exception as e:
                print(e)
                return HttpResponse(f'Failed to get post for post id: {kwargs["post_id"]}', status = status.HTTP_400_BAD_REQUEST)

    
    # DELETE /authors/{AUTHOR_UUID}/posts/{POST_UUID}
    # Wolph, October 19, https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models
    @extend_schema(
        summary = "post_delete",
        responses = PostSerializer,
        tags=['post']
    )
    @action(detail=True, methods=['delete'], url_name='delete_post')
    def delete(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        User story: As an author, I want to delete my own public posts.

        User story: As an author, other authors cannot modify my public post
        """
        try:
            if self.authorize_user(kwargs['author_id']) == False:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)
            
            post = Post.objects.get(official_id=kwargs['post_id'])
            post.delete()

            return Response(status = status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
    
    #awwester, October 19, https://stackoverflow.com/questions/31173324/django-rest-framework-update-field
    #Ameya Joshi, October 19, https://stackoverflow.com/questions/62381855/how-to-update-model-objects-only-one-field-data-when-doing-serializer-save

    @extend_schema(
        summary = "post_update",
        request = CreatePostSerializer,
        responses = PostSerializer,
        tags=['post']
    )
    @action(detail=True, methods=['POST'], url_name='post_update')
    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        update the post whose id is post_id

        User story: As an author, posts I create can be a private to my friends.

        User story: As an author, posts I make can be in simple plain text

        User story: As an author, other authors cannot modify my public post

        User story: as an author I want to edit public posts
        """
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

    #Daniel van Flymen, October 19, https://stackoverflow.com/questions/35024781/create-or-update-with-put-in-django-rest-framework
    @extend_schema(
        summary = "post_create_and_update_at_id",
        request = CreatePostSerializer,
        responses = PostSerializer,
        tags=['post']
    )
    @action(detail=True, methods=['put'], url_name='post_create_and_update')
    def put(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        update or create post whose id is post_id

        User story: as an author I want to edit public posts

        User story: As an author I want to make public posts.

        User story: As an author, other authors cannot modify my public post
        """
        instance = self.get_object_or_none()

        if self.authorize_user(kwargs['author_id']) == False:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

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
    @extend_schema(
        summary = "post_get_all_public_post",
        responses = inline_serializer(
            name='PostList',
            fields={
                'type': serializers.CharField(),
                'items': PostSerializer(many=True)
            }
        ),
        tags=['post']
    )
    @action(detail=True, methods=['get'], url_name='post_get_all_public_posts')
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        """
        User story: As an author I should be able to browse the public posts of everyone
        """
        try:
            public_posts = Post.objects.filter(
                visibility = Visibility.PUBLIC
            )
            posts = []
            for post in public_posts:
                post_with_comments = PostHelper.add_comments_and_count(author = None, post = post)
                posts.append(post_with_comments)
                
            return Response(posts)

        except Exception as e:
            print(e)
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
    
    @extend_schema(
        responses=PostSerializerList,
        summary="post_get_authors_posts",
        tags=["post", RemoteUtil.REMOTE_IMPLEMENTED_TAG, RemoteUtil.TEAM12_CONNECTED, RemoteUtil.TEAM14_CONNECTED, RemoteUtil.TEAM7_CONNECTED]
    )
    @action(detail=True, methods=['get'], url_name='post_get_author_posts')
    def get(self, request, *args, **kwargs):
        """
        Get authors posts

        User story: As an author I want to make public posts.

        User story: As an author, I want to be able to use my web-browser to manage/author my posts
        """
        node: Author = request.user
        if not node.is_authenticated:
            return HttpResponseNotFound()

        if node.is_authenticated_user:
            try:
                target_author = Author.get_author(kwargs['author_id'])
            except:
                return Response(f"Error getting author id: {kwargs['author_id']}", status.HTTP_400_BAD_REQUEST)

            #local -> local
            if target_author.is_local():
                author = Author.get_author(kwargs['author_id'])
                posts = Post.objects.filter(author = author, unlisted = False).order_by('-published')

                posts_with_comments = []
                for post in posts:
                    post_with_comments = PostHelper.add_comments_and_count(author = None, post = post)
                    posts_with_comments.append(post_with_comments)
                
                data = posts_with_comments
                data, err = PaginationHelper.paginate_serialized_data(request, data)

                if err is not None:
                    return Response(f'{err}', status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'type': 'posts', 'items': data})

            # local -> remote
            else:
                node_config = base.REMOTE_CONFIG.get(target_author.host)
                return node_config.get_authors_posts(request, request.path)

        # remote -> local
        if request.user.is_authenticated_node:
            author = Author.objects.get(official_id = kwargs['author_id'])
            posts = Post.objects.filter(author = author).order_by('-published')

            posts_with_comments = []
            for post in posts:
                post_with_comments = PostHelper.add_comments_and_count(author = None, post = post)
                posts_with_comments.append(post_with_comments)
            
            data = posts_with_comments
            data, err = PaginationHelper.paginate_serialized_data(request, data)

            if err is not None:
                return HttpResponseNotFound()
            else:
                return Response({'type': 'posts', 'items': data})


    # Édouard Lopez, October 19, https://stackoverflow.com/questions/5255913/kwargs-in-django
    @extend_schema(
        summary = "post_create_post",
        request = CreatePostSerializer,
        responses = PostSerializer,
        tags=['post']
    )
    @action(detail=True, methods=['post'], url_name='post_POST')
    def post(self, request, *args, **kwargs):
        """
        Create brand new post, no id

        As an author I want to make public posts.

        As an author, posts I create can be a private to my friends.
        
        As an author, posts I make can be in simple plain text
        """
        try:
            serializer = CreatePostSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                author = Author.get_author(kwargs['author_id'])
                data['author'] = author
                post = serializer.create(validated_data=data)
            else:
                return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

            try:
                if post.visibility == Visibility.FRIENDS:
                    inbox_post = PostSerializer(post).data
                    followers = FollowUtil.get_followers(author)
                
                    for follower in followers: 
                        if follower.is_local():
                            inbox = Inbox.objects.get(author = follower)
                            inbox.add_to_inbox(inbox_post)
                        else:
                            node_config = base.REMOTE_CONFIG.get(follower.host)
                            response = node_config.send_to_remote_inbox(target_author_url = follower.get_url(), data = inbox_post)
                            if response.status_code < 200 or response.status_code > 300:  
                                print("Did not send to remote inbox")

            except Exception as e:
                return Response(f"Error sending post to inbox, error: {e}", status = status.HTTP_400_BAD_REQUEST)

            return Response(PostSerializer(post).data, status = status.HTTP_200_OK)

        except Exception as e:
            logger.info(e)
            return HttpResponseNotFound()
class SharePostView(GenericAPIView):
    serializer_class = SharePostSerializer
    @extend_schema(
        summary = "post_share_post",
        tags=['post']
    )
    @action(detail=True, methods=['put'], url_name='post_share_post')
    def put(self, request: Request, *args, **kwargs) -> HttpResponse:
        '''
        Local wants to share local post
        Local wants to share remote post

        1. Get post 
            a) if remote, you will need to fetch post through request

        2. Get followers for the requesting author
        3. Add post to local and remote followers
        '''
        node: Author = request.user
        if not node.is_authenticated:
            return Response("You are not authenticated", status.HTTP_400_BAD_REQUEST)

        if node.is_authenticated_user:
            try:
                target_author = Author.get_author(kwargs['author_id'])
            except:
                return Response(f"Error getting author id: {kwargs['author_id']}", status.HTTP_400_BAD_REQUEST)

            #local getting a local post 
            if target_author.is_local():
                try:
                    post = PostSerializer(Post.objects.get(official_id = kwargs['post_id'])).data
                except:
                    return Response(f"Error getting post id: {kwargs['post_id']}", status.HTTP_400_BAD_REQUEST)
            #local getting a remote post
            else:
                try:
                    node_config = base.REMOTE_CONFIG.get(target_author.host)
                    response = node_config.get_post_by_post_id(request.path.split('/share')[0])
                    if response.status_code < 200 or response.status_code > 300:
                        return Response("Failed to get post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)
                    post = json.loads(response.content)
                except Exception as e:
                    print(f'{self}: put: error getting remote post: {e}')
                    return Response("Failed to get post from remote server", status.HTTP_500_INTERNAL_SERVER_ERROR)


            requesting_author = Author.get_author(self.request.user.get_id())
            followers = FollowUtil.get_followers(requesting_author)

            if len(followers) == 0:
                return Response("You currently have no followers", status = status.HTTP_202_ACCEPTED)
        
            for follower in followers: 
                if follower.is_local():
                    inbox = Inbox.objects.get(author = follower)
                    inbox.add_to_inbox(post)
                else:
                    try:
                        node_config = base.REMOTE_CONFIG.get(follower.host)
                        response = node_config.send_to_remote_inbox(target_author_url = follower.get_url(), data = post)
                        if response.status_code < 200 or response.status_code > 300:
                            return Response(json.loads(response.content), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except Exception as e:
                        print(f'{self}: put: error with remote authors: {e}')

            return Response("Successfully added to all followers inbox", status = status.HTTP_200_OK)


class FollowingPostView(GenericAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    @extend_schema(
        responses=PostSerializerList,
        summary="post_get_authors_following_posts",
        tags=["post", "follows"]
    )
    @action(detail=True, methods=['get'], url_name='post_get_authors_following_post')
    def get(self, request, *args, **kwargs):
        try:
            requesting_author = Author.get_author(kwargs['author_id'])
        except:
            return Response(f"Error getting author id: {kwargs['author_id']}", status.HTTP_400_BAD_REQUEST)

        followed_authors = FollowUtil.get_following_authors(requesting_author)
        posts = []

        # these authors could be local or remote
        for followed_author in followed_authors:
            if followed_author.is_local():
                authors_posts = Post.objects.filter(author = followed_author, unlisted = False).order_by('-published')

                for post in authors_posts:
                    post_with_comments = PostHelper.add_comments_and_count(author = requesting_author, post = post)
                    posts.append(post_with_comments)

            else:
                try:
                    node_config = base.REMOTE_CONFIG.get(followed_author.host)
                    authors_posts_path = f'/authors/{followed_author.get_id()}/posts/'
                    response = node_config.get_authors_posts(request, authors_posts_path)

                    posts = posts + response.data['items']
                except Exception as e:
                    continue

        return Response(posts, status = status.HTTP_200_OK)


class ImagePostView(GenericAPIView):
    renderer_classes = [JPEGRenderer, PNGRenderer]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    @extend_schema(
        responses=PostSerializerList,
        summary="post_get_image_post",
        tags=["post",]
    )
    @action(detail=True, methods=['get'], url_name='post_get_image_post')
    def get(self, request, *args, **kwargs):
        node: Author = request.user
        if not node.is_authenticated:
            return HttpResponseNotFound()
        
        if node.is_authenticated_user:
            try:
                target_author = Author.get_author(kwargs['author_id'])
            except:
                return Response(f"Error getting author id: {kwargs['author_id']}", status.HTTP_400_BAD_REQUEST)

            #local -> local
            if target_author.is_local():
                try:
                    post = Post.objects.get(official_id=kwargs['post_id'])
                    if not post.content:
                        return Response("This is not an image post", status = status.HTTP_400_BAD_REQUEST) 
                    
                    header, data = post.content.split(';base64,')
                    imgdata = base64.b64decode(data)
                    return Response(imgdata, status = status.HTTP_200_OK, content_type= post.contentType)

                except Exception as e:
                    print(e)
                    return HttpResponseNotFound()
            else:
                node_config = base.REMOTE_CONFIG.get(target_author.host) 
                response = node_config.get_image_post(request.path)
                return response


        # remote -> local
        if request.user.is_authenticated_node:
            post = Post.objects.get(official_id=kwargs['post_id'])
            if not post.content:
                return Response("This is not an image post", status = status.HTTP_400_BAD_REQUEST) 
            
            header, data = post.content.split(';base64,')
            imgdata = base64.b64decode(data)

            return Response(imgdata, status = status.HTTP_200_OK, content_type= post.contentType)

