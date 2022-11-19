import json

import requests
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.serializers.author_serializer import AuthorSerializer
from authors.util import AuthorUtil
from follow.models import Follow


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

    def to_internal_value(self, data):
        if 'id' not in data:
            raise serializers.ValidationError('Missing id')
        follow = Follow.objects.get(id=data['id'])
        if follow is None:
            raise serializers.ValidationError(f'Follow (id={data[id]}) does not exist')
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
