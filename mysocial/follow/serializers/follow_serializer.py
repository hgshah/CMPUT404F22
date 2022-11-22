import json

import requests
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from authors.util import AuthorUtil
from follow.models import Follow
from mysocial.settings import base


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'super actor from 9999 follows super from current server (8000)',
            value=
            {
                "type": "Follow",
                "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                "summary": "actor wants to follows super",
                "hasAccepted": True,
                "object": {
                    "type": "author",
                    "id": "cde6b179-6d0c-4efe-815e-5d6ceffd3d78",
                    "url": "http://127.0.0.1:8000/authors/cde6b179-6d0c-4efe-815e-5d6ceffd3d78",
                    "host": "127.0.0.1:8000",
                    "displayName": "super",
                    "github": "https://github.com/super/",
                    "profileImage": ""
                },
                "actor": {
                    "type": "author",
                    "id": "5e69cb89-b599-45b8-87aa-bc87adbeaed6",
                    "url": "http://127.0.0.1:9999/authors/5e69cb89-b599-45b8-87aa-bc87adbeaed6",
                    "host": "127.0.0.1:9999",
                    "displayName": "actor",
                    "github": "https://github.com/actor/",
                    "profileImage": ""
                },
                "localUrl": "http://127.0.0.1:8000/follows/497f6eca-6276-4993-bfeb-53cbbbba6f08",
                "remoteUrl": "http://127.0.0.1:9999/follows/497f6eca-6276-4993-bfeb-53cbbbba6f08"
            }
        )
    ]
)
class FollowRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    summary = serializers.SerializerMethodField('get_summary')
    hasAccepted = serializers.BooleanField(source='has_accepted')
    actor = serializers.SerializerMethodField('get_actor')
    object = serializers.SerializerMethodField('get_object')
    localUrl = serializers.SerializerMethodField('get_local_url')
    remoteUrl = serializers.SerializerMethodField('get_remote_url')

    def get_type(self, model) -> str:
        return "Follow"

    def get_summary(self, model) -> str:
        return str(model)

    @extend_schema_field(AuthorSerializer)
    def get_actor(self, model: Follow) -> dict:
        author, err = AuthorUtil.from_author_url_to_author(model.actor)
        if err is not None:
            raise ValidationError(f"Cannot find author: {model.target} with error: {err}")
        return AuthorSerializer(author).data

    @extend_schema_field(AuthorSerializer)
    def get_object(self, model: Follow) -> dict:
        author, err = AuthorUtil.from_author_url_to_author(model.target)
        if err is not None:
            raise ValidationError(f"Cannot find author: {model.target} with error: {err}")
        return AuthorSerializer(author).data

    def get_local_url(self, model: Follow):
        return model.get_local_url()

    def get_remote_url(self, model: Follow):
        return model.remote_url

    def to_internal_value(self, data: dict):
        target_serializer = AuthorSerializer(data=data['object'])
        if not target_serializer.is_valid():
            raise serializers.ValidationError('FollowRequestSerializer: to_internal_value: invalid json')
        target: Author = target_serializer.validated_data

        if target.is_local():
            try:
                # case 1: local target/object
                follow: Follow = Follow.objects.get(id=data['id'])
                follow._author_target = target
            except Follow.DoesNotExist:
                raise serializers.ValidationError('FollowRequestSerializer: to_internal_value: follow does not exist')
            except Exception as e:
                raise serializers.ValidationError(f'FollowRequestSerializer: to_internal_value: unknown error: {e}')
        else:
            # get configuration
            node_config = base.REMOTE_CONFIG.get(target.host)
            if node_config is None:
                raise serializers.ValidationError(
                    f'FollowRequestSerializer: to_internal_value: host not found: {target.host}')
            remote_fields: dict = node_config.remote_follow_fields

            # transform data to be consistent based on target host
            for remote_field, local_field in remote_fields.items():
                if remote_field not in data:
                    continue
                else:
                    data[local_field] = data[remote_field]

            # get author
            actor_serializer = AuthorSerializer(data=data['actor'])
            if not actor_serializer.is_valid():
                raise serializers.ValidationError('FollowRequestSerializer: to_internal_value: invalid json')
            actor: Author = target_serializer.validated_data

            try:
                # case 2: remote target/object that already exists
                follow = Follow.objects.get(actor=actor.get_url(), target=target.get_url())
                follow._author_target = target
                follow._author_actor = actor

                for remote_field, local_field in remote_fields.items():
                    if remote_field not in data:
                        continue
                    else:
                        setattr(follow, local_field, data[remote_field])
                follow.save()

            except Follow.DoesNotExist:
                # case 3: this is a new follow request we've made. make a local copy
                # I know... I'm putting too much faith in other servers
                # todo: add security later? lol
                follow = Follow.objects.create(
                    actor=actor.get_url(),
                    target=target.get_url(),
                    has_accepted=data['has_accepted'],
                    remote_url=data['local_url'],  # switcharoo
                    remote_id=data['proxy_id']
                )
                follow._author_target = target
                follow._author_actor = actor

            except Exception as e:
                raise serializers.ValidationError(f'FollowRequestSerializer: to_internal_value: unknown error: {e}')

        return follow

    class Meta:
        model = Follow
        fields = ('type', 'id', 'summary', 'hasAccepted', 'object', 'actor', 'localUrl', 'remoteUrl')


class FollowRequestListSerializer(serializers.ModelSerializer):
    """Only for documentation"""
    type = serializers.SerializerMethodField('get_type')
    items = FollowRequestSerializer(many=True)

    def get_type(self) -> str:
        return "Follow"

    class Meta:
        model = Follow
        fields = ('type', 'items')
