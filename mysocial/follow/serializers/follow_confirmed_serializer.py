import json

import requests
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authors.serializers.author_serializer import AuthorSerializer
from authors.util import AuthorUtil
from follow.models import Follow
from follow.serializers.follow_serializer import FollowRequestSerializer


class FollowConfirmedRequestSerializer(FollowRequestSerializer):
    hasAccepted = None
    localUrl = None
    remoteUrl = None

    class Meta:
        model = Follow
        fields = ('type', 'summary', 'object', 'actor')
