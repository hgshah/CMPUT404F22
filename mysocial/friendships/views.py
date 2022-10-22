from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from friendships.serializers.follow_serializer import FollowSerializer
from friendships.models import Follow


class FriendshipView(GenericAPIView):
    def get_queryset(self):
        return None

    def get(self, request: HttpRequest, action: str) -> HttpResponse:
        serializers: ModelSerializer = None

        if action == "create":
            # todo(turnip): create
            pass
        elif action == "destroy":
            pass
            # todo(turnip): destroy
        elif action == "incoming":
            relationships = Follow.objects.filter(target=request.user, is_pending=True)
            serializers = FollowSerializer(relationships, many=True)
        elif action == "outgoing":
            relationships = Follow.objects.filter(actor=request.user, is_pending=True)
            serializers = FollowSerializer(relationships, many=True)
        elif action == "followers":
            pass
            # todo(turnip): followers <- can be reused by the author endpoint
        elif action == "following":
            # todo(turnip): following <- can be reused by the author endpoint
            pass

        if serializers is None:
            return HttpResponseNotFound()
        else:
            return Response(data=serializers.data)
