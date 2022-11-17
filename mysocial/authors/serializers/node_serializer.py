from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer
from post.serializer import PostSerializer
from .models import Comment, ContentType
from drf_spectacular.utils import extend_schema_field

from ..models.remote_node import RemoteNode


class NodeSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        pass

    class Meta:
        model = RemoteNode
