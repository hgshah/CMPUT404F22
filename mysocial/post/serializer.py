from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer 
from .models import Post, ContentType, Visibility
from comment.models import Comment
from drf_spectacular.utils import extend_schema_field
import logging 

import logging, json
from urllib.request import urlopen

logger = logging.getLogger("mylogger")

class PostSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    @extend_schema_field(AuthorSerializer)
    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author
    
    def get_id(self, obj) -> str:
        return obj.official_id

    def get_url(self, obj: Post) -> str:
        return obj.get_url()

    def get_comments(self, obj):
        return f"{self.get_id(obj)}/comments"
    
    def get_count(self, obj):
        return Comment.objects.filter(post=obj).count()
    
    @extend_schema_field(list[str])
    def get_categories(self, obj):
        category_list = []
        
        for category in obj.categories:
            category_list.append(category)

        return category_list

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