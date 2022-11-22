from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from follow.models import Follow


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'super actor from 8080 follows super from current server (8000)',
            value=
            {
                "hasAccepted": True
            }
        )
    ]
)
class FollowAcceptSerializer(serializers.ModelSerializer):
    hasAccepted = serializers.BooleanField()

    class Meta:
        model = Follow
        fields = ('hasAccepted',)
