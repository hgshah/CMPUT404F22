import logging

from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from common.pagination_helper import PaginationHelper

logger = logging.getLogger(__name__)


class AuthorView(GenericViewSet):
    pagination_class = None

    def get_queryset(self):
        return

    @staticmethod
    @extend_schema(
        responses=inline_serializer(
            name='AuthorList',
            fields={
                'type': serializers.CharField(),
                'items': AuthorSerializer(many=True)
            }
        ),
        summary="authors_retrieve_all"
    )
    @action(detail=True, methods=['get'], url_name='retrieve_all')
    def retrieve_all(request: Request):
        # lazy query set serialization so it's fine if this goes first
        # todo(turnip): only allow superusers because this kinda seems bad access?
        authors = Author.objects.all()
        serializer = AuthorSerializer(
            authors,
            many=True,
            context={
                "host": request.get_host()
            })
        data = serializer.data

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            logger.info("AuthorView: _get_all_authors:", err)
            return HttpResponseNotFound()

        return Response({
            'type': 'authors',
            'items': data
        })

    @staticmethod
    @extend_schema(
        responses=AuthorSerializer,
        summary="authors_retrieve"
    )
    def retrieve(request: Request, author_id: str) -> HttpResponse:
        try:
            author = Author.objects.get(official_id=author_id)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        serializer = AuthorSerializer(
            author,
            context={
                "host": request.get_host()
            })
        return Response(serializer.data)
