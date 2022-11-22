import pathlib
from urllib.parse import urlparse

from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework import serializers

from authors.models.author import Author
from common.base_util import BaseUtil
from mysocial.settings import base

AUTHOR_SERIALIZER_EXAMPLE = {
    "type": "author",
    "id": "9ae19cc1-4fbe-478a-bcbf-ffddbf906605",
    "url": "http://127.0.0.1:8080/authors/9ae19cc1-4fbe-478a-bcbf-ffddbf906605",
    "host": "127.0.0.1:8080",
    "displayName": "super",
    "github": "https://github.com/super/",
    "profileImage": ""
}


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon author',
            value=AUTHOR_SERIALIZER_EXAMPLE,
        ),
    ]
)
class AuthorSerializer(serializers.ModelSerializer):
    """
    Author object
    """
    type = serializers.SerializerMethodField('get_type')
    """Test"""
    id = serializers.SerializerMethodField('get_id')
    displayName = serializers.CharField(source='display_name')
    profileImage = serializers.CharField(source='profile_image')
    url = serializers.SerializerMethodField('get_url')
    host = serializers.SerializerMethodField('get_host')

    @staticmethod
    def get_type(model: Author) -> str:
        return model.get_serializer_field_name()

    @staticmethod
    def get_url(model: Author) -> str:
        # they're the same as id, for now
        return model.get_url()

    @staticmethod
    def get_id(model: Author) -> str:
        """Tests"""
        # the path after host may vary, e.g. authors/ vs authors/id
        return str(model.official_id)

    @staticmethod
    def get_host(model: Author) -> str:
        if model.host == '':
            return base.CURRENT_DOMAIN

        return model.host

    def to_internal_value(self, data: dict) -> Author:
        """
        Does not work with remote Author
        :param data:
        :return: Access serializers.validated_data for deserialized version of the json converted to Author
        """

        for required_field in AuthorSerializer.Meta.required_fields:
            if required_field not in data:
                raise serializers.ValidationError(f'AuthorSerializer: missing field: {required_field}')

        url = data['url']
        # by Philipp Claßen from https://stackoverflow.com/a/56476496/17836168
        _, host, path, _, _, _ = urlparse(url)

        try:
            if host == base.CURRENT_DOMAIN:
                local_id = pathlib.PurePath(path).name
                # deserialize a local author
                author = Author.objects.get(official_id=local_id)
            else:
                # deserialize a remote author; it's missing some stuff so check with is_local()
                author = Author()
                node_config = base.REMOTE_CONFIG.get(host)
                if node_config is None:
                    print(f"AuthorSerializer: Host not found: {host}")
                    return serializers.ValidationError(f"AuthorSerializer: Host not found: {host}")
                remote_fields: dict = node_config.remote_author_fields

                for remote_field, local_field in remote_fields.items():
                    if remote_field not in data:
                        continue
                    elif remote_field == 'url':
                        # special case
                        sanitized: str = data[remote_field]
                        for start in ('http://', 'https://'):
                            if sanitized.startswith(start):
                                sanitized = sanitized[len(start):]
                        prefix = BaseUtil.get_http_or_https()
                        setattr(author, local_field, f'{prefix}{sanitized}')
                    else:
                        setattr(author, local_field, data[remote_field])
                author.host = host  # force a set even if field was not given
        except Exception as e:
            print(f"AuthorSerializer: failed serializing: {e}")
            raise serializers.ValidationError(f"AuthorSerializer: failed serializing: {e}")

        return author

    class Meta:
        model = Author
        fields = ('type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage')

        # custom fields
        required_fields = ('url',)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon author list',
            value={
                'type': 'authors',
                'items': [AUTHOR_SERIALIZER_EXAMPLE],
            },
        ),
    ]
)
class AuthorSerializerList(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    items = AuthorSerializer(many=True, read_only=True)

    @staticmethod
    def get_type(model: Author) -> str:
        return model.get_serializer_field_name()

    class Meta:
        model = Author
        fields = ('type', 'items')


# trick to prevent circular dependency
Author.SERIALIZER = AuthorSerializer
