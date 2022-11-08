from rest_framework import serializers

from authors.serializers.author_serializer import AuthorSerializer
from follow.models import Follow


class FollowRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    summary = serializers.SerializerMethodField('get_summary')
    actor = AuthorSerializer(read_only=True)
    object = AuthorSerializer(source='target', read_only=True)
    hasAccepted = serializers.BooleanField(source='has_accepted')

    def get_type(self, model) -> str:
        return "Follow"

    def get_summary(self, model) -> str:
        return str(model)

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
