from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer
from post.serializer import PostSerializer 
from .models import Comment, ContentType

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    id = serializers.SerializerMethodField()
    comment = serializers.CharField()
    published = serializers.DateTimeField()
    author = serializers.SerializerMethodField()
    contentType = serializers.ChoiceField(ContentType)

    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author
    
    def get_post(self, obj):
        post = PostSerializer(obj.post).data
        return post

    def get_id(self, obj):
        post_id = PostSerializer(obj.post).data["id"]
        return f"{post_id}/comments/{obj.official_id}"

    class Meta:
        model = Comment
        fields = ('type', 'author', 'comment', 'contentType', 'published', 'id')

class CreateCommentSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
    class Meta:
        model = Comment
        fields =('comment', 'contentType')