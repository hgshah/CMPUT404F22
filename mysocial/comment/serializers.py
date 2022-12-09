from rest_framework import serializers
from post.serializer import PostSerializer 
from .models import Comment, ContentType
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer

from rest_framework import serializers
from comment.models import Comment
from authors.models.author import Author
from urllib.parse import urlparse
from mysocial.settings import base
import pathlib
from post.models import Post
from authors.serializers.author_serializer import AuthorSerializer

COMMENT_SERIALIZER_EXAMPLE = {
        "type": "comment",
        "author": {
            "type": "author",
            "id": "f4af2492-e84f-4d4d-87fa-3832bc17b953",
            "url": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953",
            "host": "127.0.0.1:8080",
            "displayName": "chris",
            "github": "",
            "profileImage": ""
        },
        "comment": "ehe",
        "contentType": "text/plain",
        "published": "2022-11-19T23:35:13.662908Z",
        "id": "f58d1f1f-a8e2-4adc-a75c-9a5bdbe34eb7",
        "url": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953/posts/4e7adec8-0ed5-48fc-ad75-058a349c0fd4/comments/f58d1f1f-a8e2-4adc-a75c-9a5bdbe34eb7"
    }
@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon COMMENT Object',
            value=COMMENT_SERIALIZER_EXAMPLE,
        ),
    ]
)
class CommentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    published = serializers.DateTimeField()
    contentType = serializers.ChoiceField(ContentType)
    url = serializers.SerializerMethodField()
    
    def get_id(self, obj) -> str:
        return str(obj.official_id)

    def get_url(self, obj: Comment) -> str:
        return obj.get_url()

    @extend_schema_field(PostSerializer)
    def get_post(self, obj):
        post = PostSerializer(obj.post).data
        return post

    def to_internal_value(self, data: dict) -> Comment:
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
                comment = Comment.objects.get(official_id = local_id)
            else:
                # deserialize a remote author; take not it's missing some stuff so check with is_local()
                comment = Comment()
                node_config = base.REMOTE_CONFIG.get(host)
                if node_config is None:
                    print(f"CommentSerializer: Host not found: {host}")
                    return serializers.ValidationError(f"CommentSerializer: Host not found: {host}")

                comment_remote_fields: dict = node_config.comment_remote_fields
        
                for remote_field, local_field in comment_remote_fields.items():
                    if remote_field not in data:
                        continue
                    elif remote_field == 'author':
                        author = Author.get_author(official_id=data['author']['id'], should_do_recursively=True)
                        setattr(comment, local_field, AuthorSerializer(author).data)
                    else:
                        setattr(comment, local_field, data[remote_field])

        except Exception as e:
            print(f"CommentSerializer: failed serializing {e}")
            raise serializers.ValidationError(f"CommentSerializer: failed serializing {e}")

        post = Post.objects.first()
        setattr(comment, 'post', post) # looool, we don't actually include that post that the comment is on so im faking it, its just a get so i don't think anything happens??
        return comment

    class Meta:
        model = Comment
        fields = ('type', 'author', 'comment', 'contentType', 'published', 'id', 'url')

class CreateCommentSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(allow_blank = True, required = False)

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
    class Meta:
        model = Comment
        fields =('comment', 'contentType', 'actor')

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon Comment list',
            value={
                'type': 'comment',
                'items': [COMMENT_SERIALIZER_EXAMPLE],
            },
        ),
    ]
)
class CommentSerializerList(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    items = CommentSerializer(many=True, read_only=True)

    @staticmethod
    def get_type(model: Comment) -> str:
        return model.get_serializer_field_name()

    class Meta:
        model = Comment
        fields = ('type', 'items')


class InboxCommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    author = serializers.JSONField()
    comment = serializers.CharField()
    published = serializers.CharField()
    contentType = serializers.ChoiceField(ContentType)
    id = serializers.CharField()
    url = serializers.CharField()

    class Meta:
        model = Comment
        fields = ('type', 'author', 'comment', 'contentType', 'published', 'id', 'url')
    