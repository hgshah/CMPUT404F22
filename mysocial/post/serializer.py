from rest_framework import serializers
from authors.models import Author
from authors.serializers.author_serializer import AuthorSerializer 
from .models import Post, ContentType, Visibility
import logging 
logger = logging.getLogger("mylogger")

class PostSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    id = serializers.SerializerMethodField()
    title = serializers.CharField()
    source = serializers.URLField()
    origin = serializers.URLField()
    #categories = serializers.ListField()
    published = serializers.DateTimeField()
    description = serializers.CharField()
    unlisted = serializers.BooleanField()
    author = serializers.SerializerMethodField()
    visibility = serializers.ChoiceField(Visibility)
    contentType = serializers.ChoiceField(ContentType)

    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author
    
    def get_id(self, obj):
        author_id = AuthorSerializer(obj.author).data["id"]
        return f"{author_id}/posts/{obj.official_id}"

    class Meta:
        model = Post
        fields = ('type', 'title', 'id', 'source', 'origin', 'description','contentType', 'author', 'published', 'visibility', 'unlisted')

class CreatePostSerializer(serializers.ModelSerializer,):
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post

    class Meta:
        model = Post
        fields = ('title', 'description','visibility','source', 'origin', 'contentType', 'unlisted')