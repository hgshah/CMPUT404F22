from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer 
from .models import Post, ContentType, Visibility
from comment.models import Comment
from authors.models.author import Author
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from urllib.parse import urlparse
from mysocial.settings import base
import pathlib


POST_SERIALIZER_EXAMPLE = {
    "type": "post",
    "title": "mytitle",
    "id": "aa292f41-90b2-4b0f-af4e-fc4cdfaabcc4",
    "source": "",
    "origin": "",
    "description": "mydesc",
    "contentType": "text/plain",
    "author": {
        "type": "author",
        "id": "44248451-2deb-421c-b5f6-db0c214b68ea",
        "url": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea",
        "host": "127.0.0.1:8000",
        "displayName": "amanda",
        "github": "",
        "profileImage": ""
    },
    "categories": [],
    "count": 1,
    "comments": "aa292f41-90b2-4b0f-af4e-fc4cdfaabcc4/comments",
    "published": "2022-11-17T21:07:41.803434Z",
    "visibility": "public",
    "unlisted": False,
    "url": "http://127.0.0.1:8000/authors/44248451-2deb-421c-b5f6-db0c214b68ea/posts/aa292f41-90b2-4b0f-af4e-fc4cdfaabcc4"
}
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon POST Object',
            value=POST_SERIALIZER_EXAMPLE,
        ),
    ]
)
class PostSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    source = serializers.CharField(default = "www.default.com")
    origin = serializers.CharField(default = "www.default.com")

    @extend_schema_field(AuthorSerializer)
    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author
    
    def get_id(self, obj) -> str:
        return str(obj.official_id)

    def get_url(self, obj: Post) -> str:
        return obj.get_url()

    def get_comments(self, obj):
        return f"{self.get_url(obj)}/comments"
    
    def get_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    @extend_schema_field(list[str])
    def get_categories(self, obj):
        category_list = []
        
        for category in obj.categories:
            category_list.append(category)

        return category_list
    
    def to_internal_value(self, data: dict) -> Post:
        """
        Does not work with remote Author
        :param data:
        :return: Access serializers.validated_data for deserialized version of the json converted to Author
        """
        url = data['url']
        # by Philipp Claßen from https://stackoverflow.com/a/56476496/17836168
        _, host, path, _, _, _ = urlparse(url)

        try:
            if host == base.CURRENT_DOMAIN:
                local_id = pathlib.PurePath(path).name
                # deserialize a local post
                post = Post.objects.get(official_id=local_id)
            else:
                # deserialize a remote author; take not it's missing some stuff so check with is_local()
                post = Post()
                node_config = base.REMOTE_CONFIG.get(host)
                if node_config is None:
                    print(f"PostSerializer: Host not found: {host}")
                    return serializers.ValidationError(f"PostSerializer: Host not found: {host}")
                post_remote_fields: dict = node_config.post_remote_fields
   
                for remote_field, local_field in post_remote_fields.items():
                    if remote_field not in data:
                        continue
                    elif remote_field == 'author':
                        author = Author.get_author(official_id=data['author']['id'], should_do_recursively=True)
                        setattr(post, local_field, author)
                    elif remote_field == 'source' or remote_field == 'origin':
                        if not data[remote_field]:
                            continue
                    else:
                        setattr(post, local_field, data[remote_field])

        except Exception as e:
            print(f"PostSerializer: failed serializing {e}")
            raise serializers.ValidationError(f"PostSerializer: failed serializing {e}")

        return post

    class Meta:
        model = Post
        fields = ('type', 'title', 'id', 'source', 'origin','description','contentType',  'author', 'categories', 'count', 'comments', 'published', 'visibility', 'unlisted', 'url')

class CreatePostSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
    class Meta:
        model = Post
        fields = ('title', 'description','visibility','source', 'origin', 'categories', 'contentType', 'unlisted')

class SharePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon Posts list',
            value={
                'type': 'post',
                'items': [POST_SERIALIZER_EXAMPLE],
            },
        ),
    ]
)
class PostSerializerList(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    items = PostSerializer(many=True, read_only=True)

    @staticmethod
    def get_type(model: Post) -> str:
        return model.get_serializer_field_name()

    class Meta:
        model = Post
        fields = ('type', 'items')

# Created to make fields required when someone tries to add a post to inbox
class InboxPostSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    title = serializers.CharField()
    id = serializers.CharField()
    source = serializers.CharField(default = "www.default.com")
    origin = serializers.CharField(default = "www.default.com")
    description = serializers.CharField()
    contentType = serializers.ChoiceField(ContentType)
    author = serializers.JSONField()
    categories = serializers.ListField(default = [])
    count = serializers.IntegerField()
    comments = serializers.CharField()
    published = serializers.CharField()
    visibility = serializers.CharField()
    unlisted = serializers.BooleanField(default = False)
    url = serializers.CharField()

    class Meta:
        model = Post
        fields = ('type', 'title', 'id', 'source', 'origin', 'description', 'contentType',  'author', 'categories', 'count', 'comments', 'published', 'visibility', 'unlisted', 'url')
