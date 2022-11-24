import logging

import requests
from django.db import IntegrityError
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from authors.util import AuthorUtil
from common.pagination_helper import PaginationHelper
from follow.follow_util import FollowUtil
from follow.models import Follow
from follow.serializers.follow_accept_serializer import FollowAcceptSerializer
from follow.serializers.follow_serializer import FollowRequestListSerializer, FollowRequestSerializer
from mysocial.settings import base
from remote_nodes.node_config_base import NodeConfigBase
from remote_nodes.remote_util import RemoteUtil

logger = logging.getLogger(__name__)


# todo(turnip): Refactor when tests are available

class OutgoingRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowRequestListSerializer

    def get_queryset(self):
        return None

    @staticmethod
    @extend_schema(
        parameters=PaginationHelper.OPEN_API_PARAMETERS,
        summary="outgoing_follow_requests_all"
    )
    def get(request: Request) -> HttpResponse:
        """Get all outgoing follow requests that were not accepted yet"""
        relationships = Follow.objects.filter(actor=request.user.get_url(), has_accepted=False)
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
    @extend_schema(
        parameters=PaginationHelper.OPEN_API_PARAMETERS,
        summary="incoming_follow_requests_all"
    )
    def get(request: Request) -> HttpResponse:
        """
        Get all incoming follow requests

        User story: as an author: I want to un-befriend local and remote authors.

        User story: as an author: I want to know if I have friend requests.

        User story: as an author, When I befriend someone (they accept my friend request) I follow them, only when the
        other author befriends me do I count as a real friend – a bi-directional follow is a true friend.

        User story: As an author, I want to befriend local authors

        See the step-by-step calls to follow or befriend someone at:
        https://github.com/hgshah/cmput404-project/blob/main/endpoints.txt#L137
        """
        relationships = Follow.objects.filter(target=request.user.get_url(), has_accepted=False)
        serializers = FollowRequestSerializer(relationships, many=True)
        data, err = PaginationHelper.paginate_serialized_data(request, serializers.data)
        if err is not None:
            return HttpResponseNotFound()
        return Response(data={
            'type': 'followRequests',
            'items': data,
        })


class IndividualRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        return None

    @staticmethod
    @extend_schema(
        tags=['possibly-deprecating'],
    )
    def get(request: Request, follow_id: str = None) -> HttpResponse:
        """
        Get an individual follow request

        User story: as an author: I want to un-befriend local and remote authors.
        todo(turnip): remote authors not yet implemented

        User story: as an author, When I befriend someone (they accept my friend request) I follow them, only when the
        other author befriends me do I count as a real friend – a bi-directional follow is a true friend.
        todo(turnip): remote authors not yet implemented

        User story: As an author, I want to befriend local authors

        See the step-by-step calls to follow or befriend someone at:
        https://github.com/hgshah/cmput404-project/blob/main/endpoints.txt#L137
        """
        try:
            follow: Follow = Follow.objects.get(id=follow_id)
            user_url = request.user.get_url()
            if follow.target != user_url and follow.actor != user_url:
                # Only the two accounts should be able to delete an account
                # Returning not found due to security concerns
                return HttpResponseNotFound()

            # if remote_url is present, and we are not authoritative, sync!
            if follow.remote_url != '' and follow.actor == user_url:
                # todo(turnip): get Follow object from remote
                # todo(turnip): update our current Follow object
                pass

            serializers = FollowRequestSerializer(follow)
            return Response(data=serializers.data)
        except Follow.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            print(f'IncomingRequestPutView: put: unknown error: {e}')
            return HttpResponseBadRequest()

    @staticmethod
    @extend_schema(
        tags=['possibly-deprecating'],
    )
    def put(request: Request, follow_id: str = None) -> HttpResponse:
        """
        Accept a follow request
        Only the target or object can accept the actor's request.
        This is only one way. You cannot make a follow back into has_accepted = False, you have to delete it.

        User story: as an author: I want to un-befriend local and remote authors.
        todo(turnip): remote authors not yet implemented

        User story: as an author, When I befriend someone (they accept my friend request) I follow them, only when the
        other author befriends me do I count as a real friend – a bi-directional follow is a true friend.
        todo(turnip): remote authors not yet implemented

        See the step-by-step calls to follow or befriend someone at:
        https://github.com/hgshah/cmput404-project/blob/main/endpoints.txt#L137
        """
        # todo(turnip): implement case where remote node informs us that our Follow request was accepted

        try:
            follow = Follow.objects.get(id=follow_id)
            if follow.target != request.user.get_url():
                # Only the two accounts should be able to delete an account
                # Returning not found due to security concerns
                return HttpResponseNotFound()
            if Follow.FIELD_NAME_HAS_ACCEPTED not in request.data \
                    or not request.data[Follow.FIELD_NAME_HAS_ACCEPTED]:
                # You cannot make a follow back into has_accepted = False, you have to delete it.
                return HttpResponseBadRequest()

            follow.has_accepted = True
            follow.save()

            # todo(turnip): update the Follow reference from the remote server

            serializers = FollowRequestSerializer(follow)
            return Response(data=serializers.data)
        except Follow.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            print(f'IncomingRequestPutView: put: unknown error: {e}')
            return HttpResponseBadRequest()

    @staticmethod
    @extend_schema(
        tags=['possibly-deprecating'],
        responses={
            200: OpenApiResponse(response=FollowRequestSerializer)
        }
    )
    def delete(request: Request, follow_id: str = None) -> HttpResponse:
        """
        Delete, decline, or cancel a follow request

        User story: as an author: I want to un-befriend local and remote authors.
        todo(turnip): remote authors not yet implemented
        """
        if not request.user.is_authenticated:
            return HttpResponseNotFound()

        try:
            follow: Follow = Follow.objects.get(id=follow_id)
            if follow.target != request.user.get_url() and follow.actor != request.user.get_url():
                # Only the two accounts should be able to delete an account
                # Returning not found due to security concerns
                return HttpResponseNotFound()

            follow.delete()

            # todo(turnip): if remote, delete Follow reference or mirror from the remote server

            return Response()
        except Follow.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            print(f'IncomingRequestPutView: put: unknown error: {e}')
            return HttpResponseBadRequest()


class FollowersView(APIView):
    def get_queryset(self):
        return None

    def get_serializer_class(self):
        return FollowRequestSerializer

    @staticmethod
    @extend_schema(
        parameters=RemoteUtil.REMOTE_NODE_MULTIL_PARAMS,
        summary='get_all_followers',
        tags=['follows', RemoteUtil.REMOTE_IMPLEMENTED_TAG],
        responses=inline_serializer(
            name='Followers',
            fields={
                'type': serializers.CharField(),
                'items': AuthorSerializer(many=True)
            }
        )
    )
    def get(request: Request, author_id: str = None) -> HttpResponse:
        """
        Get followers for an Author

        See the step-by-step calls to follow or befriend someone at:
        https://github.com/hgshah/cmput404-project/blob/main/endpoints.txt#L137

        User story: As an author, my server will know about my friends
        """
        try:
            author = Author.get_author(author_id)
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        except Exception as e:
            print(f"FollowersView: get: unknown errr: {e}")
            return HttpResponseNotFound()

        if not author.is_local():
            return FollowersView.get_remote(request, author, request.query_params)

        user = None
        try:
            user = Author.get_author(official_id=author_id)
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
    def get_remote(request: Request, author: Author, params: dict):
        node_config: NodeConfigBase = base.REMOTE_CONFIG.get(author.host)
        if node_config is None:
            return HttpResponseNotFound()
        return node_config.get_all_followers_request(author=author, params=params)

    @staticmethod
    @extend_schema(
        parameters=RemoteUtil.REMOTE_NODE_MULTIL_PARAMS,
        summary='create follow request (post followers)',
        tags=['follows', RemoteUtil.REMOTE_IMPLEMENTED_TAG],
        request=inline_serializer(
            name='FollowRequestRequest',
            fields={
                'actor': serializers.URLField(allow_null=True)
            }
        ),
        responses=FollowRequestSerializer(),
    )
    def post(request: Request, author_id: str = None) -> HttpResponse:
        """
        Create a follow request for an author

        There three are cases:
        1. A local author makes a follow request to a local author
            - Do an **auth** call with a user credential
            - **author_id** is the local author
        2. A remote node tells us that one of its users wants to follow us
            - Do an **auth** call with a node/server credential
            - Add an `actor` in the json payload in the request body
            - **author_id** is the local author they want to follow
        3. A local author makes a follow request to a remote author
            - Do an **auth** with a user credential
            - **author_id** is the remote author

        For more details, check out: https://github.com/hgshah/cmput404-project/pull/89

        User story: as an author: I want to un-befriend local and remote authors.

        User story: as an author, When I befriend someone (they accept my friend request) I follow them, only when the
        other author befriends me do I count as a real friend – a bi-directional follow is a true friend.

        See the step-by-step calls to follow or befriend someone at:
        https://github.com/hgshah/cmput404-project/blob/main/endpoints.txt#L137
        """
        if not request.user.is_authenticated:
            return HttpResponseNotFound()

        if request.user.is_authenticated_user:
            # let's figure out if we want to follow someone local or remote
            try:
                target_author = Author.get_author(author_id)
            except Author.DoesNotExist:
                return HttpResponseNotFound()
            except Exception as e:
                print(f"FollowersView: Unknown error: {e}")
                return HttpResponseNotFound()

            if target_author.is_local():
                return FollowersView.post_local_follow_local(request, author_target=target_author)
            else:
                return FollowersView.post_local_follow_remote(request, author_target=target_author)

        if request.user.is_authenticated_node:
            # a remote node tells us that one of its users wants to follow someone in our server
            return FollowersView.post_remote_follow_local(request, author_id=author_id)

        return HttpResponseForbidden()

    @staticmethod
    def post_local_follow_local(request: Request, author_target: Author) -> HttpResponse:
        author_actor: Author = request.user
        data = None
        try:
            if author_target == author_actor:
                # validation: do not follow self!
                return HttpResponseBadRequest('You can not follow self')

            follow = Follow.objects.create(
                actor=author_actor.get_url(),
                target=author_target.get_url(),
                has_accepted=False)
            serializers = FollowRequestSerializer(follow)
            data = serializers.data
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        except IntegrityError:
            return HttpResponseBadRequest('You\'re either following this account or have already made a follow request')
        except Exception as e:
            print(f'FollowersView: post: unknown error: {e}')
            return HttpResponseBadRequest()
        return Response(data=data)

    @staticmethod
    def post_local_follow_remote(request: Request, author_target: Author) -> HttpResponse:
        node_config = base.REMOTE_CONFIG.get(author_target.host)
        if node_config is None:
            print(f"post_local_follow_remote: missing config for host: {author_target.host}")
            return HttpResponseNotFound()
        response_json = node_config.post_local_follow_remote(request.user.get_url(), author_target)
        if isinstance(response_json, int):
            return Response(status=response_json)
        try:
            actor_json = response_json['actor']
            target_json = response_json['object']
            # todo: refactor this to accommodate for other server mapping
            follow = Follow.objects.create(
                actor=actor_json['url'],
                target=target_json['url'],
                has_accepted=response_json['hasAccepted'],
                remote_url=response_json['localUrl'],
                remote_id=response_json['id']
            )
            serializers = FollowRequestSerializer(follow)
            data = serializers.data
        except Author.DoesNotExist:
            return HttpResponseNotFound()
        except IntegrityError:
            return HttpResponseBadRequest('You\'re either following this account or have already made a follow request')
        except Exception as e:
            print(f'FollowersView: post_local_follow_remote: post: unknown error: {e}')
            return HttpResponseBadRequest()
        return Response(data=data)

    @staticmethod
    def post_remote_follow_local(request: Request, author_id: str = None) -> HttpResponse:
        """
        a remote node tells us that one of its users wants to follow someone in our server

        payload should have author url of the author that wants to follow

        :param request:
        :param author_id:
        :return:
        """
        # todo: clean up code?
        target = None
        data = None
        try:
            actor_url = request.data['actor']
            actor, err = AuthorUtil.from_author_url_to_author(actor_url)
            if err is not None:
                print(f'FollowersView: post_remote_follow_local: Author cannot be found: {actor_url}')
                return HttpResponseNotFound(
                    f'FollowersView: post_remote_follow_local: Author cannot be found: {actor_url}')

            actor: Author = actor
            target = Author.get_author(official_id=author_id)
            follow = Follow.objects.create(
                actor=actor.get_url(),
                target=target.get_url(),
                has_accepted=False)
            serializers = FollowRequestSerializer(follow)
            data = serializers.data
        except Author.DoesNotExist:
            print(f"Local author does not exist: {author_id}")
            return HttpResponseNotFound()
        except IntegrityError as e:
            print(f'Integrity error: {e}')
            return HttpResponseBadRequest('You\'re either following this account or have already made a follow request')
        except Exception as e:
            print(f'FollowersView: post: unknown error: {e}')
            return HttpResponseBadRequest()
        return Response(data=data)


class FollowersIndividualView(GenericAPIView):
    def get_queryset(self):
        return None

    def get_serializer_class(self):
        return FollowRequestSerializer

    def get_follow(request: Request, target_id: str, follower_id: str) -> (Follow, HttpResponse):
        """Helper function to getting a follow regardless of local or remote"""
        author: Author = request.user

        if not (author.is_authenticated_node or author.get_id()
                == str(target_id) or author.get_id()
                == str(follower_id)):
            return None, HttpResponseForbidden()

        try:
            target = Author.get_author(official_id=target_id)
        except Follow.DoesNotExist:
            return None, HttpResponseNotFound("User not exist on our end")
        except Exception as e:
            print(f"FollowersIndividualView: {e}")
            return None, HttpResponseNotFound("User not exist on our end")

        try:
            follower = Author.get_author(official_id=follower_id)
        except Follow.DoesNotExist:
            return None, HttpResponseNotFound(
                "The given follower does not seem to exist as a user in any connected nodes")
        except Exception as e:
            print(f"FollowersIndividualView: {e}")
            return None, HttpResponseNotFound("The given follower does not seem to exist as a user")

        if target.is_local():
            # trust our data
            try:
                follow = Follow.objects.get(target=target.get_url(), actor=follower.get_url())

                if follow.get_author_target() != request.user and not follow.has_accepted:
                    return None, HttpResponseNotFound("User does not follow the following author on our end")

                return follow, None
            except Follow.DoesNotExist:
                return None, HttpResponseNotFound("User does not follow the following author on our end")
            except Exception as e:
                print(f"FollowersIndividualView: {e}")
                return None, HttpResponseNotFound("User does not follow the following author on our end")
        else:
            # trust THEIR data
            node_config = base.REMOTE_CONFIG.get(target.host)
            if node_config is None:
                print(f"FollowersIndividualView: get: unknown host: {target.host}")
                return None, HttpResponseNotFound()

            follow = node_config.get_remote_follow(target, follower)
            if follow is None:
                return None, HttpResponseNotFound("User does not follow the following author on our end")

            return follow, None

    @staticmethod
    @extend_schema(
        summary="get follower or check if follower",
        tags=['follows', RemoteUtil.REMOTE_IMPLEMENTED_TAG]
    )
    def get(request: Request, target_id: str, follower_id: str) -> HttpResponse:
        """
        Check if follower_id is a follower of author_id.

        This is for public consumption ONLY if it's true that the follower follows the author.

        Otherwise, you may only access this if you are the following:
        - A remote node/server (please, we trust you lol)
        - The follower which is a local author
        - The object/actor which is a local author

        **author_id:** ID of the author we want to check followers of
        **follower_id:** ID of the author we want to check is a follower of author with author_id

        https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#followers
        GET [local, remote] check if FOREIGN_AUTHOR_ID is a follower of AUTHOR_ID

        PR with example: https://github.com/hgshah/cmput404-project/pull/99
        More details about the fields returned at: https://github.com/hgshah/cmput404-project/blob/staging/mysocial/follow/serializers/follow_serializer.py
        """
        follow, error_response = FollowersIndividualView.get_follow(request, target_id, follower_id)
        if follow is None:
            return error_response

        follow_serializer = FollowRequestSerializer(follow)
        follow_json = follow_serializer.data

        if follow.has_accepted:
            # public information
            return Response(follow_json)
        elif not request.user.is_authenticated:
            # not logged in
            return Response(status=401)
        elif request.user.is_authenticated_node or request.user == follow.get_author_actor() or request.user == follow.get_author_target():
            # oh, you're one of the parties involved, go ahead
            return Response(follow_json)
        else:
            # you shouldn't be snooping
            return HttpResponseForbidden()

    @staticmethod
    @extend_schema(
        summary="Accept follow request",
        tags=['follows'],
        request=FollowAcceptSerializer()
    )
    def put(request: Request, target_id: str, follower_id: str):
        """
        To accept a follow request, an author must explicitly indicate that they are accepting it by adding a payload
        with the boolean hasAccepted = true. Checkout the payload example below

        https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#followers
        PUT [local]: Add FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID (must be authenticated)

        Behavior: if already accepted follow request, and you call this indicating accepting follow request, just return 200 again.
        """
        if not request.user.is_authenticated:
            return Response(401)

        follow, error_response = FollowersIndividualView.get_follow(request, target_id, follower_id)
        if follow is None:
            return error_response
        follow: Follow = follow  # type hint

        if follow.get_author_target() != request.user:
            # you're not allowed!
            return HttpResponseForbidden()

        has_accepted = request.data.get('hasAccepted') in ['True', 'true']
        if has_accepted is None or not isinstance(has_accepted, bool):
            return HttpResponseBadRequest("Missing boolean hasAccepted payload")

        if not has_accepted:
            return HttpResponseBadRequest("Cannot downgrade a follow request or follow status. Use DELETE. If wanted "
                                          "to accept, set hasAccepted = true.")

        # accept!
        follow.has_accepted = True
        follow.save()

        follow_serializer = FollowRequestSerializer(follow)
        follow_json = follow_serializer.data
        return Response(follow_json)

    @staticmethod
    @extend_schema(
        summary="Decline or delete follow request",
        tags=['follows', RemoteUtil.REMOTE_IMPLEMENTED_TAG],
        responses={
            200: OpenApiResponse(response=FollowRequestSerializer)
        }
    )
    def delete(request: Request, target_id: str, follower_id: str):
        """
        The following can remove the follower in the follow list of an author:
        - The follower (actor)
        - The author being followed (object/target)
        - A remote server/node but only if one of tthe actor or object belongs to theirs

        https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#followers
        DELETE [local]: remove FOREIGN_AUTHOR_ID as a follower of AUTHOR_ID
        """
        if not request.user.is_authenticated:
            return Response(401)

        follow, error_response = FollowersIndividualView.get_follow(request, target_id, follower_id)
        if follow is None:
            return error_response
        follow: Follow = follow  # type hint
        target = follow.get_author_target()
        actor = follow.get_author_actor()

        if target != request.user and actor != request.user and not request.user.is_authenticated_node:
            # you're not allowed!
            return HttpResponseForbidden()

        # protection against bad server
        if request.user.is_authenticated_node:
            host = request.user.host
            if host != target.host and host != actor.host:
                return HttpResponseForbidden()

        # we gotta make sure, remote server isn't sending us inbox anymore!
        if not target.is_local():
            node_config: NodeConfigBase = base.REMOTE_CONFIG.get(target.host)
            if node_config is None:
                print(f"FollowersIndividualView: delete: cannot find node_config: {target.host}")
                return HttpResponseNotFound()
            # todo
            response = node_config.delete_local_follow_remote(author_target=follow.get_author_target(),
                                                              author_actor=follow.get_author_actor())
            if response is int:
                print(f"Delete: unknown status code: {response}")
                return HttpResponseBadRequest("Struggling to communicate with the other server T.T")

        follow_serializer = FollowRequestSerializer(follow)
        follow_json = follow_serializer.data
        follow_json['summary'] = 'Deleted'

        # delete
        follow.delete()

        return Response(follow_json)


# todo(turnip): add test
class RealFriendsView(GenericAPIView):
    def get_queryset(self):
        return None

    def get_serializer_class(self):
        return FollowRequestSerializer

    @staticmethod
    @extend_schema(
        parameters=PaginationHelper.OPEN_API_PARAMETERS,
        responses=inline_serializer(
            name='RealFriends',
            fields={
                'type': serializers.CharField(),
                'items': AuthorSerializer(many=True)
            }
        ),
        tags=['follows'],
        summary='get_all_real_friends'
    )
    def get(request: Request, author_id: str = None) -> HttpResponse:
        """
        Get mutual friends, real friends, true friends, or mutual followers for an Author

        User story: as an author, When I befriend someone (they accept my friend request) I follow them, only when the
        other author befriends me do I count as a real friend – a bi-directional follow is a true friend.
        todo(turnip): remote authors not yet implemented

        User story: As an author, posts I create can be a private to my friends.

        User story: As an author, my server will know about my friends
        """
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
