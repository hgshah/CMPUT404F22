from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
import logging
from common.simple_auth import SimpleAuth

# models
from .models import Inbox
from authors.models.author import Author
from inbox.models import ItemType

# serializing
from inbox.serializers import InboxSerializer, AllInboxSerializer
from post.serializer import PostSerializer
from comment.serializers import CommentSerializer
from follow.serializers.follow_serializer import FollowRequestSerializer

logger = logging.getLogger("mylogger")

class InboxView(GenericAPIView):
    serializer_class = InboxSerializer

    def get_queryset(self):
        return Inbox.objects.all()

    def post(self, request: Request, *args, **kwargs) -> HttpResponse:
        try:
            author = Author.objects.get(official_id = kwargs['author_id'])
            inbox = Inbox.objects.get(author = author)
            
            self.validate_request_data(request)

            inbox.add_to_inbox(request.data)
            serializer = InboxSerializer(inbox)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return HttpResponseNotFound()


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
            serializer = InboxSerializer(inbox)
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