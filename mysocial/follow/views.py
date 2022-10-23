import logging

from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from authors.models import Author
from authors.serializers.author_serializer import AuthorSerializer
from common import PaginationHelper
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer

logger = logging.getLogger(__name__)


# todo(turnip): create
# todo(turnip): destroy
# todo(turnip): followers <- can be reused by the author endpoint
# todo(turnip): following <- can be reused by the author endpoint

class OutgoingRequestView(GenericAPIView):
    def get_queryset(self):
        return None

    @staticmethod
    def get(request: Request) -> HttpResponse:
        relationships = Follow.objects.filter(actor=request.user, is_pending=True)
        serializers = FollowRequestSerializer(relationships, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data=data)


class IncomingRequestView(GenericAPIView):
    def get_queryset(self):
        return None

    @staticmethod
    def get(request: Request) -> HttpResponse:
        relationships = Follow.objects.filter(target=request.user, is_pending=True)
        serializers = FollowRequestSerializer(relationships, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data=data)


class FollowersView(GenericAPIView):
    def get_queryset(self):
        return None

    @staticmethod
    def get(request: Request, author_id: str = None) -> HttpResponse:
        """Get followers for author_id"""
        user = None
        try:
            user = Author.objects.get(official_id=author_id)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        follow_ids = Follow.objects.values_list('actor', flat=True).filter(target=user, is_pending=False)
        followers = Author.objects.filter(official_id__in=follow_ids)
        serializers = AuthorSerializer(followers, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data={
            'type': 'followers',
            'items': data,
        })
