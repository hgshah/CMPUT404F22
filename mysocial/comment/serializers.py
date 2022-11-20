from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer
from post.serializer import PostSerializer 
from .models import Comment, ContentType
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer

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
    author = serializers.SerializerMethodField()
    contentType = serializers.ChoiceField(ContentType)
    url = serializers.SerializerMethodField()

    @extend_schema_field(AuthorSerializer)
    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author
    
    @extend_schema_field(PostSerializer)
    def get_post(self, obj):
        post = PostSerializer(obj.post).data
        return post

    def get_id(self, obj: Comment):
        return obj.get_id()

    def get_url(self, obj: Comment):
        return obj.get_url()

    class Meta:
        model = Comment
        fields = ('type', 'author', 'comment', 'contentType', 'published', 'id', 'url')

class CreateCommentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
    class Meta:
        model = Comment
        fields =('comment', 'contentType')

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