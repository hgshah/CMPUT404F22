import logging

from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from common import PaginationHelper
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer

logger = logging.getLogger(__name__)


class OutgoingRequestView(GenericAPIView):
    def get_queryset(self):
        return None

    def get(self, request: HttpRequest) -> HttpResponse:
        relationships = Follow.objects.filter(actor=request.user, is_pending=True)
        serializers = FollowRequestSerializer(relationships, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data=data)


class IncomingRequestView(GenericAPIView):
    def get_queryset(self):
        return None

    def get(self, request: Request) -> HttpResponse:
        relationships = Follow.objects.filter(target=request.user, is_pending=True)
        serializers = FollowRequestSerializer(relationships, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data=data)
