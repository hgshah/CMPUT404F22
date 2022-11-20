from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from likes.models import Like

LIKE_SERIALIZER_EXAMPLE = {
    "type": "Like",
    "summary": "chris likes your post",
    "author": {
        "id": "f4af2492-e84f-4d4d-87fa-3832bc17b953",
        "url": "http://127.0.0.1:8080/authors/f4af2492-e84f-4d4d-87fa-3832bc17b953",
        "host": "127.0.0.1:8080",
        "type": "author",
        "github": "",
        "displayName": "chris",
        "profileImage": ""
    },
    "object": "http://127.0.0.1:8000/authors/fa08c97f-7046-477d-ab66-c988fff92678/posts/610353f2-0ec0-4cc1-944f-67b15f01202c/"
}

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon Like Object',
            value=LIKE_SERIALIZER_EXAMPLE,
        ),
    ]
)
class LikeSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    
    def get_summary(self, obj):
        display_name = obj.author.get('displayName')
        return f'{display_name} likes your {obj.object_type}'
    class Meta:
        model = Like
        fields = ('type', 'summary', 'author', 'object')


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Socioecon liked list',
            value={
                'type': 'liked',
                'items': [LIKE_SERIALIZER_EXAMPLE],
            },
        ),
    ]
)
class LikeSerializerList(serializers.ModelSerializer):
    type = serializers.SerializerMethodField('get_type')
    items = AuthorSerializer(many=True, read_only=True)

    @staticmethod
    def get_type(model: Like) -> str:
        return model.get_serializer_field_name()

    class Meta:
        model = Like
        fields = ('type', 'items')