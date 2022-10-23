import logging

from django.db import IntegrityError
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from authors.models import Author
from authors.serializers.author_serializer import AuthorSerializer
from common import PaginationHelper
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer

logger = logging.getLogger(__name__)


# todo(turnip): destroy
# todo(turnip): following <- can be reused by the author endpoint

class OutgoingRequestView(GenericAPIView):
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
        return Response(data=data)


class IncomingRequestView(GenericAPIView):
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
        return Response(data=data)


class IncomingRequestIndividualView(GenericAPIView):
    def get_queryset(self):
        return None

    def get_serializer_class(self):
        return FollowRequestSerializer

    @staticmethod
    def get(request: Request, follow_id: str = None) -> HttpResponse:
        """Get an individual follow request"""
        try:
            follow = Follow.objects.get(id=follow_id)
            if follow.target != request.user:
                # instead of forbidden, it's not found because there was no such request for user
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
                # Other accounts cannot modify a follow on your behalf
                return HttpResponseForbidden()
            if Follow.FIELD_NAME_HAS_ACCEPTED not in request.data \
                    and request.data[Follow.FIELD_NAME_HAS_ACCEPTED]:
                # You cannot make a follow back into has_accepted = True, you have to delete it.
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
        follow_ids = Follow.objects.values_list('actor', flat=True).filter(target=user, has_accepted=True)
        followers = Author.objects.filter(official_id__in=follow_ids)
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
        return Response(data=data)
