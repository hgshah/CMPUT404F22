import logging

from django.db import IntegrityError
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from common.pagination_helper import PaginationHelper
from follow.follow_util import FollowUtil
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestListSerializer, FollowRequestSerializer
from rest_framework import serializers

logger = logging.getLogger(__name__)


# todo(turnip): Refactor when tests are available

class OutgoingRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowRequestListSerializer

    def get_queryset(self):
        return None

    @staticmethod
    def get(request: Request) -> HttpResponse:
        """Get all outgoing follow requests that were not accepted yet"""
        relationships = Follow.objects.filter(actor=request.user, has_accepted=False)
        serializers = FollowRequestSerializer(relationships, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data={
            'type': 'followRequests',
            'items': data,
        })


class IncomingRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowRequestListSerializer

    def get_queryset(self):
        return None

    @staticmethod
    def get(request: Request) -> HttpResponse:
        """Get all incoming follow requests"""
        relationships = Follow.objects.filter(target=request.user, has_accepted=False)
        serializers = FollowRequestSerializer(relationships, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data={
            'type': 'followRequests',
            'items': data,
        })


class IndividualRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        return None

    @staticmethod
    def get(request: Request, follow_id: str = None) -> HttpResponse:
        """Get an individual follow request"""
        try:
            follow = Follow.objects.get(id=follow_id)
            if follow.target != request.user and follow.actor != request.user:
                # Only the two accounts should be able to delete an account
                # Returning not found due to security concerns
                return HttpResponseNotFound()
            serializers = FollowRequestSerializer(follow)
            return Response(data=serializers.data)
        except Follow.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            logger.error(f'IncomingRequestPutView: put: unknown error: {e}')
            return HttpResponseBadRequest()

    @staticmethod
    def put(request: Request, follow_id: str = None) -> HttpResponse:
        """
        Accept a follow request
        Only the target or object can accept the actor's request.
        This is only one way. You cannot make a follow back into has_accepted = False, you have to delete it.
        """
        try:
            follow = Follow.objects.get(id=follow_id)
            if follow.target != request.user:
                # Only the two accounts should be able to delete an account
                # Returning not found due to security concerns
                return HttpResponseNotFound()
            if Follow.FIELD_NAME_HAS_ACCEPTED not in request.data \
                    or not request.data[Follow.FIELD_NAME_HAS_ACCEPTED]:
                # You cannot make a follow back into has_accepted = False, you have to delete it.
                return HttpResponseBadRequest()

            follow.has_accepted = True
            follow.save()
            serializers = FollowRequestSerializer(follow)
            return Response(data=serializers.data)
        except Follow.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            logger.error(f'IncomingRequestPutView: put: unknown error: {e}')
            return HttpResponseBadRequest()

    @staticmethod
    def delete(request: Request, follow_id: str = None) -> HttpResponse:
        """
        Delete, decline, or cancel a follow request
        """
        if not request.user.is_authenticated:
            return HttpResponseNotFound()

        try:
            follow = Follow.objects.get(id=follow_id)
            if follow.target != request.user and follow.actor != request.user:
                # Only the two accounts should be able to delete an account
                # Returning not found due to security concerns
                return HttpResponseNotFound()

            follow.delete()
            return Response(status=204)
        except Follow.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            logger.error(f'IncomingRequestPutView: put: unknown error: {e}')
            return HttpResponseBadRequest()


class FollowersView(GenericAPIView):
    def get_queryset(self):
        return None

    def get_serializer_class(self):
        return FollowRequestSerializer

    @staticmethod
    def get(request: Request, author_id: str = None) -> HttpResponse:
        """Get followers for an Author"""
        user = None
        try:
            user = Author.objects.get(official_id=author_id)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        # reference: https://stackoverflow.com/a/9727050/17836168
        followers = FollowUtil.get_followers(user)
        serializers = AuthorSerializer(followers, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data={
            'type': 'followers',
            'items': data,
        })

    @staticmethod
    def post(request: Request, author_id: str = None) -> HttpResponse:
        """
        Create a follow request for the author
        Only the current authenticated user can send request for itself
        - In other words, you can't follow request on behalf of another user
        """
        if not request.user.is_authenticated:
            return HttpResponseNotFound()

        actor = request.user
        target = None
        data = None
        try:
            target = Author.objects.get(official_id=author_id)
            if target == actor:
                # validation: do not follow self!
                return HttpResponseBadRequest('You can not follow self')

            follow = Follow.objects.create(actor=actor, target=target, has_accepted=False)
            serializers = FollowRequestSerializer(follow)
            data = serializers.data
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        except IntegrityError:
            return HttpResponseBadRequest('You\'re either following this account or have already made a follow request')
        except Exception as e:
            logger.error(f'FollowersView: post: unknown error: {e}')
            return HttpResponseBadRequest()
        return Response(data=data, status=201)


# todo(turnip): add test
class RealFriendsView(GenericAPIView):
    def get_queryset(self):
        return None

    def get_serializer_class(self):
        return FollowRequestSerializer

    @staticmethod
    @extend_schema(
        responses=inline_serializer(
            name='RealFriends',
            fields={
                'type': serializers.CharField(),
                'items': AuthorSerializer(many=True)
            }
        )
    )
    def get(request: Request, author_id: str = None) -> HttpResponse:
        """Get friends for an Author"""
        user = None
        try:
            user = Author.objects.get(official_id=author_id)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        friends = FollowUtil.get_real_friends(actor=user)
        serializers = AuthorSerializer(friends, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data={
            'type': 'realFriends',
            'items': data,
        })
