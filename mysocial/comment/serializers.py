from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer
from post.serializer import PostSerializer 
from .models import Comment, ContentType
from drf_spectacular.utils import extend_schema_field

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    published = serializers.DateTimeField()
    author = serializers.SerializerMethodField()
    contentType = serializers.ChoiceField(ContentType)

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