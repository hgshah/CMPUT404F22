import json

import requests
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.serializers.author_serializer import AuthorSerializer
from follow.models import Follow


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
        response = requests.get(model.actor)
        if response.status_code != 200:
            raise ValidationError(f"Cannot find author: {model.actor} with code {response.status_code}")
        return json.loads(response.content.decode('utf-8'))
        # future code: I want local Author and author to have the same properties
        # author_url = model.actor
        # author, err = AuthorUtil.from_author_url_to_author(author_url)
        # if err is not None:
        #     raise err
        # return AuthorSerializer(author).data

    @extend_schema_field(AuthorSerializer)
    def get_object(self, model: Follow) -> dict:
        response = requests.get(model.target)
        if response.status_code != 200:
            raise ValidationError(f"Cannot find author: {model.target} with code {response.status_code}")
        return json.loads(response.content.decode('utf-8'))

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
