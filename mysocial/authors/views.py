import logging

from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authors.models.author import Author
from authors.permissions import NodeIsAuthenticated
from authors.serializers.author_serializer import AuthorSerializer
from common.pagination_helper import PaginationHelper

logger = logging.getLogger(__name__)


# Note: GenericViewSet allows more flexibility to specify which function a method should call
# Check out author/urls.py about how we redirected get calls to retrieve and retrieve_all

class AuthorView(GenericViewSet):
    # removes the extra outer array enveloping the real request return structure
    pagination_class = None

    def get_queryset(self):
        return None

    @staticmethod
    @extend_schema(
        parameters=PaginationHelper.OPEN_API_PARAMETERS,
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
        """Gets all authors"""

        # lazy query set serialization so it's fine if this goes first
        # todo(turnip): only allow superusers because this kinda seems bad access?
        authors = Author.get_all_authors()
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
        """Get an individual author"""
        try:
            author = Author.get_author(official_id=author_id)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        serializer = AuthorSerializer(
            author,
            context={
                "host": request.get_host()
            })
        return Response(serializer.data)

    def get(self, request: Request, author_id: str = None) -> HttpResponse:
        if author_id is None:
            return self._get_all_authors(request)
        else:
            return self._get_author(request, author_id)


class RemoteNodeView(GenericAPIView):
    """
    View for other groups to test if they have a registered, active node.

    Useful for debugging and "sanity-checking" with other groups.
    """

    permission_classes = [NodeIsAuthenticated]

    def get_queryset(self):
        return None

    @staticmethod
    def get(request) -> HttpResponse:
        return Response({
            'type': 'remoteNode',
            'message': 'Authentication passed!'
        })
