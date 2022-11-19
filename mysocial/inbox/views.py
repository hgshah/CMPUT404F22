from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
import logging
from common.simple_auth import SimpleAuth
from remote_nodes.remote_util import RemoteUtil
from mysocial.settings import base
from authors.util import AuthorUtil

# models
from .models import Inbox
from authors.models.author import Author
from inbox.models import ItemType
from likes.models import Like, LikeType

# serializing
from inbox.serializers import InboxSerializer, AllInboxSerializer
from post.serializer import PostSerializer
from comment.serializers import CommentSerializer
from follow.serializers.follow_serializer import FollowRequestSerializer
from authors.serializers.author_serializer import AuthorSerializer
from likes.serializers import LikeSerializer

logger = logging.getLogger("mylogger")

class InboxView(GenericAPIView):
    serializer_class = InboxSerializer

    def get_queryset(self):
        return Inbox.objects.all()

    def post(self, request: Request, *args, **kwargs) -> HttpResponse: 
        """
        We first need to decide if what we want to add to our inbox is:
        1. Like object
        2. Post object
        3. Comment object
        4. Follow object

        From there, you split off into:
        1. Local user adding to local inbox
        2. Local user adding to remote inbox
        3. Remote user adding to local inbox
        """
        try:
            node: Author = request.user
            if not node.is_authenticated:
                return HttpResponseNotFound()
            
            type = request.data['type'].lower()

            if type == ItemType.LIKE:
                return self.handle_likes(request, node, **kwargs)
                
        except Exception as e:
            print(e)
            return HttpResponseNotFound()
    
    def handle_likes(self, request, node, **kwargs):
        if node.is_authenticated_user:
            node_target, _ = RemoteUtil.extract_node_target(request)
            # local -> local
            if node_target is None:
                return self.local_likes_local(request, target_author_id = kwargs['author_id'])
            # local -> remote
            else:
                return self.local_likes_remote(request, remote_author_id = kwargs['author_id'], node_target = node_target)

        # remote -> local
        if request.user.is_authenticated_node:
            return self.remote_likes_local(request, **kwargs)

    
    def local_likes_remote(self, request, remote_author_id, node_target):
        '''
        A local author wants to send something to a remote author

        1. Get request author from our DB
        2. Create a like
            2.a) You need to append an "actor" field, with the full author url 
        3. Send to a remote inbox using requests

        '''
        node_config = base.REMOTE_CONFIG.get(node_target)
        if node_config is None:
            print(f"post_local_likes_remote: missing config: {node_target}")
            return Response(f"post_local_likes_remote: missing config: {node_target}", status.HTTP_400_BAD_REQUEST)
        
        # step one
        try:
            requesting_author_id = self.request.user.official_id
            requesting_author = Author.objects.get(official_id = requesting_author_id)
            json_author = AuthorSerializer(requesting_author).data 
        except:
            return Response(f"Could not get local author {requesting_author_id}", status = status.HTTP_400_BAD_REQUEST)

        # step two
        like_data = self.create_like(request, json_author = json_author, actor_author_id = requesting_author_id)
        if like_data is None:
            return Response(f"Could not create Like object", status = status.HTTP_400_BAD_REQUEST)

        # step 2.A
        actor_author_id = self.request.user.official_id
        actor_author = Author.objects.get(official_id = actor_author_id)
        like_data["actor"] = AuthorSerializer(actor_author).data["url"]

        # step 3
        target_url = node_config.from_author_id_to_url(remote_author_id)
        response = node_config.send_to_remote_inbox(data = like_data, target_author_url = target_url)

        if response < 200 or response > 200:
            return Response("Failed to send to remote inbox", status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(f"Successfully added 'LIKE' to {remote_author_id}", status = status.HTTP_200_OK)
    
    def local_likes_local(self, request, target_author_id):
        '''
        A local author wants to send something to a local author

        1. Get request author from our DB
        2. Create a like
        3. Send to inbox in our DB
        '''
        # step one
        try:
            requesting_author_id = self.request.user.official_id
            requesting_author = Author.objects.get(official_id = requesting_author_id)
            json_author = AuthorSerializer(requesting_author).data
        except:
            return Response(f"Could not get local author {requesting_author_id}", status = status.HTTP_400_BAD_REQUEST)

        # step two 
        like_data = self.create_like(request, json_author = json_author, actor_author_id = requesting_author_id)
        if like_data is None:
            return Response(f"Could not create Like object", status = status.HTTP_400_BAD_REQUEST)

        # step three
        try:
            target_author = Author.objects.get(official_id = target_author_id)
            inbox = Inbox.objects.get(author = target_author)
            inbox.add_to_inbox(like_data) 
        except:
            return Response(f"Could not add to inbox for local author id: {target_author_id}", status = status.HTTP_400_BAD_REQUEST)

        return Response(f"Successfully added 'LIKE' to author {target_author.display_name} inbox", status = status.HTTP_200_OK)
    
    def remote_likes_local(self, request, **kwargs):
        '''
        A remote author wants to send something to a local author

        1. Get request author using request
        2. Create Like
        3. Send to inbox in our db 
        '''
        # step one 
        try:
            requesting_actor_url = request.data['actor'] 
            requesting_author = AuthorUtil.from_author_url_to_author(requesting_actor_url)[0] 
            requesting_author_id = AuthorUtil.from_author_url_to_local_id(requesting_actor_url) 
            json_author = AuthorSerializer(requesting_author).data 
        except:
            return Response(f"Could not get remote requesting author from url: {requesting_actor_url}", status = status.HTTP_400_BAD_REQUEST)
        
        # step two
        like_data = self.create_like(request, json_author = json_author, actor_author_id = requesting_author_id)
        if like_data is None:
            return Response(f"Could not create Like object", status = status.HTTP_400_BAD_REQUEST)
        
        # step three
        try:
            target_author = Author.objects.get(official_id = kwargs["author_id"])
            inbox = Inbox.objects.get(author = target_author)
            inbox.add_to_inbox(like_data) 
        except:
            return Response(f"Could not add to inbox for author id: {kwargs['author_id']}", status = status.HTTP_400_BAD_REQUEST)
            
        return Response(f"Successfully added 'LIKE' to author {target_author.display_name} inbox", status = status.HTTP_200_OK)

    
    def create_like(self, request, json_author, actor_author_id):
        object_id = request.data.get('object')

        if "comment" in object_id:
            object_type = LikeType.COMMENT
        else:
            object_type = LikeType.POST

        try:
            like = Like.objects.create(author = json_author, author_id = actor_author_id, object = object_id, object_type = object_type) 
            return LikeSerializer(like).data

        except Exception as e:
            print(e)
            return None

    ## GET /authors/{AUTHOR_ID}/inbox
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            if SimpleAuth.authorize_user(kwargs['author_id'], request) == False:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

            author = Author.objects.get(official_id = kwargs['author_id'])
            inbox = Inbox.objects.get(author = author)
            serializer = InboxSerializer(inbox)
            return Response(serializer.data, status = status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return HttpResponseNotFound()
    
    # DELETE /authors/{AUTHOR_ID}/inbox
    def delete(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            if SimpleAuth.authorize_user(kwargs['author_id'], request) == False:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

            author = Author.objects.get(official_id = kwargs['author_id'])
            inbox = Inbox.objects.get(author = author)
            inbox.items = []
            inbox.save()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return HttpResponseNotFound()

    def validate_request_data(self, request):
        type = request.data['type'].lower()

        if (type == ItemType.POST):
            PostSerializer(request.data)
        elif (type == ItemType.COMMENT):
            CommentSerializer(request.data)
        elif (type == ItemType.FOLLOW):
            FollowRequestSerializer(request.data)

class AllInboxView(GenericAPIView):
    serializer_class = AllInboxSerializer

    ## GET /authors/{AUTHOR_ID}/inbox/all
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            if SimpleAuth.authorize_user(kwargs['author_id'], request) == False:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

            author = Author.objects.get(official_id = kwargs['author_id'])
            inbox = Inbox.objects.get(author = author)
            serializer = AllInboxSerializer(inbox)
            return Response(serializer.data, status = status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return HttpResponseNotFound()