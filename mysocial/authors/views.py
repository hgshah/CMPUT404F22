import logging

from django.http.response import HttpResponse, HttpResponseNotFound
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from authors.models.author import Author
from authors.permissions import NodeIsAuthenticated
from authors.serializers.author_serializer import AuthorSerializer, AuthorSerializerList
from common.base_util import BaseUtil
from common.pagination_helper import PaginationHelper
from mysocial.settings import base
from remote_nodes.remote_util import RemoteUtil

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
        parameters=PaginationHelper.OPEN_API_PARAMETERS + RemoteUtil.REMOTE_NODE_SINGLE_PARAMS,
        responses=AuthorSerializerList,
        summary="Authors retrieve all",
        tags=["authors", RemoteUtil.REMOTE_IMPLEMENTED_TAG]
    )
    @action(detail=True, methods=['get'], url_name='retrieve_all')
    def retrieve_all(request: Request):
        """
        Gets all authors (remote or local)

        If the request was from an anonymous user or is a local user, we return users from both local and remote.

        If the request was from a **node**, we only return local users.
        """
        node_target, other_params = RemoteUtil.extract_node_target(request)
        if node_target is not None:
            return AuthorView.retrieve_all_remote(request, node_target, other_params)

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

        # look at everyone else
        # do not recursively find an author if this is a node
        should_do_recursively = not (request.user.is_authenticated and request.user.is_authenticated_node)
        if should_do_recursively:
            for node in BaseUtil.connected_nodes:
                author_jsons = node.get_all_author_jsons(request.query_params)
                if author_jsons is None:
                    print(f'AuthorsView: cannot connect: {node.domain}')
                else:
                    data += author_jsons

        data, err = PaginationHelper.paginate_serialized_data(request, data)

        if err is not None:
            logger.info("AuthorView: _get_all_authors:", err)
            return HttpResponseNotFound()

        return Response({
            'type': 'authors',
            'items': data
        })

    @staticmethod
    def retrieve_all_remote(request: Request, node_param: str, params: dict):
        """Gets all authors in another node
        :param node_param: node domain
        :param request: http request
        :param params: other query params; useful for pagination
        """
        node_config = base.REMOTE_CONFIG.get(node_param)
        if node_config is None:
            return HttpResponseNotFound()
        return node_config.get_all_authors_request(params)

    @staticmethod
    @extend_schema(
        parameters=RemoteUtil.REMOTE_NODE_SINGLE_PARAMS,
        responses=AuthorSerializer,
        summary="Retrieve an author",
        tags=["authors", RemoteUtil.REMOTE_IMPLEMENTED_TAG]
    )
    def retrieve(request: Request, author_id: str) -> HttpResponse:
        """
        Get an individual author

        If the request was from an anonymous user or is a local user, we return try find the author locally and remotely.

        If the request was from a **node**, we only return local users.
        """

        node_target, _ = RemoteUtil.extract_node_target(request)
        if node_target is not None:
            return AuthorView.retrieve_author(request, node_target, author_id)

        try:
            # do not recursively find an author if this is a node
            should_do_recursively = not (request.user.is_authenticated and request.user.is_authenticated_node)
            author = Author.get_author(official_id=author_id, should_do_recursively=should_do_recursively)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        serializer = AuthorSerializer(
            author,
            context={
                "host": request.get_host()
            })
        return Response(serializer.data)

    @staticmethod
    def retrieve_author(request: Request, node_param: str, author_id: str):
        """Get an author in another node"""
        node_config = base.REMOTE_CONFIG.get(node_param)
        if node_config is None:
            return HttpResponseNotFound()
        return node_config.get_author_request(author_id)


class AuthorSelfView(APIView):
    permission_classes = [IsAuthenticated]
    serializers = AuthorSerializer

    def get_queryset(self):
        return None

    @staticmethod
    @extend_schema(
        parameters=PaginationHelper.OPEN_API_PARAMETERS,
        summary="Get current author logged in details"
    )
    def get(request: Request) -> HttpResponse:
        """Get details about the current author"""
        return Response(AuthorSerializer(request.user).data)


class RemoteNodeView(GenericAPIView):
    """
    View for other groups to test if they have a registered, active node.

    Useful for debugging and "sanity-checking" with other groups.

    To use basic auth, do the following:
    GET https://username:password@www.socioecon.herokuapp.com/remote-node/
    """

    permission_classes = [NodeIsAuthenticated]

    def get_queryset(self):
        return None

    @staticmethod
    @extend_schema(
        tags=["remote-debug", RemoteUtil.REMOTE_IMPLEMENTED_TAG]
    )
    def get(request) -> HttpResponse:
        return Response({
            'type': 'remoteNode',
            'message': 'Authentication passed!'
        })
