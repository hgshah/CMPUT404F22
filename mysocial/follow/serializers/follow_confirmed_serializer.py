import json

import requests
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.serializers.author_serializer import AuthorSerializer
from authors.util import AuthorUtil
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'super actor from 8080 follows super from current server (8000)',
            value=
            {
                "type": "Follow",
                "summary": "actor follows super",
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
                    "url": "http://127.0.0.1:8080/authors/5e69cb89-b599-45b8-87aa-bc87adbeaed6",
                    "host": "127.0.0.1:8080",
                    "displayName": "actor",
                    "github": "https://github.com/actor/",
                    "profileImage": ""
                }
            }
        )
    ]
)
class FollowConfirmedRequestSerializer(FollowRequestSerializer):
    hasAccepted = None
    localUrl = None
    remoteUrl = None

    class Meta:
        model = Follow
        fields = ('type', 'summary', 'object', 'actor')
