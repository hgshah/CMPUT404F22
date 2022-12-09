import json
import pathlib
from urllib.parse import urlparse

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
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

    Note:
        - displayName: the name the user explicitly wanted to be known
        - preferredName: the name the user defaults to when there's no displayName
    """
    type = serializers.SerializerMethodField('get_type')
    id = serializers.SerializerMethodField('get_id')
    displayName = serializers.CharField(source='display_name')
    profileImage = serializers.CharField(source='profile_image')
    url = serializers.SerializerMethodField('get_url')
    host = serializers.SerializerMethodField('get_host')
    preferredName = serializers.SerializerMethodField('get_preferred_name')

    SPECIAL_SHOULD_TRUST_LOCAL_TAG = 'should_trust_local'

    # check node_config_base.py for duplicate; can't ref due to circular dependency
    CHANGEABLE_FIELDS = {
        'displayName': 'display_name',
        'github': 'github',
        'profileImage': 'profile_image',
        'email': 'email',
        'username': 'username',
        'password': 'password',
    }

    @staticmethod
    def get_type(model: Author) -> str:
        return model.get_serializer_field_name()

    @staticmethod
    def get_url(model: Author) -> str:
        # they're the same as id, for now
        return model.get_url()

    @staticmethod
    def get_id(model: Author) -> str:
        # the path after host may vary, e.g. authors/ vs authors/id
        return str(model.official_id)

    @staticmethod
    def get_host(model: Author) -> str:
        if model.host == '':
            return base.CURRENT_DOMAIN

        return model.host

    @staticmethod
    def get_preferred_name(model: Author) -> str:
        return str(model)

    def to_internal_value(self, data: dict) -> Author:
        """
        Converts the give author url to an author, either remote or local.

        If data contains a True boolean SPECIAL_SHOULD_TRUST_LOCAL_TAG, the local author's fields will be
        overwritten. This saves the author automatically.

        :param data:
        :return: Access serializers.validated_data for deserialized version of the json converted to Author
        """

        # validation, we need url!!!
        if 'url' not in data:
            # try to get url via host
            if 'host' in data and 'id' in data:
                host = data['host']
                # there's a better solution but since this is a one-off, I won't do that
                if '127.0.0.1' in base.CURRENT_DOMAIN and host == 'https://true-friends-404.herokuapp.com':
                    host = '127.0.0.1:8012'
                    data['host'] = host
                elif 'true-friends-404.herokuapp.com' in host:
                    host = 'true-friends-404.herokuapp.com'
                    data['host'] = host

                author_id = data['id']
                data['url'] = f'{BaseUtil.get_http_or_https()}{host}/authors/{author_id}'
                data_url = data['url']

            if 'url' not in data:
                raise serializers.ValidationError({'url': 'missing_field'})

        url = data['url']
        # by Philipp Claßen from https://stackoverflow.com/a/56476496/17836168
        _, host, path, _, _, _ = urlparse(url)

        try:
            if host == base.CURRENT_DOMAIN:
                local_id = pathlib.PurePath(path).name
                # deserialize a local author
                author = Author.objects.get(official_id=local_id)

                # trust the fields given
                should_trust = bool(data.get(AuthorSerializer.SPECIAL_SHOULD_TRUST_LOCAL_TAG))
                if should_trust:
                    for client_field, server_field in AuthorSerializer.CHANGEABLE_FIELDS.items():
                        if client_field in data:
                            if server_field == 'password':
                                author.set_password(data[client_field])
                            else:
                                setattr(author, server_field, data[client_field])

                    # saving for should trust
                    try:
                        author.save()
                    except Exception as e:
                        raise serializers.ValidationError({'non_field_errors': str(e)})
            else:
                # deserialize a remote author; it's missing some stuff so check with is_local()
                author = Author()
                node_config = base.REMOTE_CONFIG.get(host)
                if node_config is None:
                    print(f"AuthorSerializer: Host not found: {host}")
                    raise serializers.ValidationError({host: 'missing field'})
                remote_fields: dict = node_config.remote_author_fields

                for remote_field, local_field in remote_fields.items():
                    if remote_field not in data:
                        continue

                    entry = data[remote_field]

                    # post-processing
                    if local_field == 'github':
                        # team14 case
                        if entry.strip() != '' and 'https://github.com/' not in entry:
                            entry = f'https://github.com/{entry}/'
                    elif local_field == 'url':
                        # special case
                        sanitized: str = data[remote_field]
                        for start in ('http://', 'https://'):
                            if sanitized.startswith(start):
                                sanitized = sanitized[len(start):]
                        prefix = BaseUtil.get_http_or_https()
                        entry = f'{prefix}{sanitized}'

                    setattr(author, local_field, entry)
                    # end loop for processing and setting entries

                author.host = host  # force a set even if field was not given

                # special processing for team7
                if node_config.team_metadata_tag == 'team7' and 'id' in data:
                    author_id = data['id']
                    entry = f'{BaseUtil.get_http_or_https()}{node_config.domain}/service/authors/{author_id}'
                    setattr(author, 'url', entry)

                # special processing for team12
                if node_config.team_metadata_tag == 'team12':
                    author_url = data['url']
                    setattr(author, 'url', f'{author_url}/')
                    author.username = author.display_name
        except Exception as e:
            print(f"AuthorSerializer: failed serializing: {e}")
            raise serializers.ValidationError({'non_field_errors': str(e)})

        return author

    class Meta:
        model = Author
        fields = ('type', 'id', 'url', 'host', 'displayName', 'github', 'profileImage', 'preferredName')

    @classmethod
    def deserializer_author_list(cls, response_json: str):
        if isinstance(response_json, str):
            author_json = json.loads(response_json)
        elif isinstance(response_json, dict) or isinstance(response_json, list):
            author_json = response_json
        else:
            print(f'AuthorSerializer: deserializer_author_list: unknown type ({type(response_json)}): {str(response_json)}')
            return []

        if isinstance(author_json, dict):
            author_json = author_json.get('items')

        if author_json is None:
            print('AuthorSerializer: deserializer_author_list: author_json is None')
            return []

        author_list = []
        for raw_author in author_json:
            author_deserializer = AuthorSerializer(data=raw_author)
            if author_deserializer.is_valid():
                author = author_deserializer.validated_data
                author_list.append(AuthorSerializer(author).data)
            else:
                print(f'AuthorSerializer: deserializer_author_list: unknown error')
        return author_list


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
