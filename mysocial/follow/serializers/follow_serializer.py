from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from authors.models.author import from_author_url_to_author
from authors.serializers.author_serializer import AuthorSerializer
from follow.models import Follow


class FollowRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    summary = serializers.SerializerMethodField('get_summary')
    hasAccepted = serializers.BooleanField(source='has_accepted')
    actor = serializers.SerializerMethodField('get_actor')
    object = serializers.SerializerMethodField('get_object')

    def get_type(self, model) -> str:
        return "Follow"

    def get_summary(self, model) -> str:
        return str(model)

    @extend_schema_field(AuthorSerializer)
    def get_actor(self, model: Follow) -> ReturnDict:
        author_url = model.actor
        author, err = from_author_url_to_author(author_url)
        if err is not None:
            raise err
        return AuthorSerializer(author).data

    @extend_schema_field(AuthorSerializer)
    def get_object(self, model: Follow) -> ReturnDict:
        author_url = model.target
        author, err = from_author_url_to_author(author_url)
        if err is not None:
            raise err
        return AuthorSerializer(author).data

    def to_internal_value(self, data):
        if 'id' not in data:
            raise serializers.ValidationError('Missing id')
        follow = Follow.objects.get(id=data['id'])
        if follow is None:
            raise serializers.ValidationError(f'Follow (id={data[id]}) does not exist')
        return follow

    class Meta:
        model = Follow
        fields = ('type', 'id', 'summary', 'hasAccepted', 'object', 'actor')


class FollowRequestListSerializer(serializers.ModelSerializer):
    """Only for documentation"""
    type = serializers.SerializerMethodField('get_type')
    items = FollowRequestSerializer(many=True)

    def get_type(self) -> str:
        return "Follow"

    class Meta:
        model = Follow
        fields = ('type', 'items')
