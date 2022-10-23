from rest_framework import serializers

from authors.serializers.author_serializer import AuthorSerializer
from follow.models import Follow


class FollowRequestSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    summary = serializers.SerializerMethodField('get_summary')
    actor = AuthorSerializer(read_only=True)
    object = AuthorSerializer(source='target', read_only=True)

    def get_type(self, model):
        return "Follow"

    def get_summary(self, model):
        return str(model)

    class Meta:
        model = Follow
        fields = ('type', 'summary', 'has_accepted', 'object', 'actor')
