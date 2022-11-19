# models
from .models import Inbox
from authors.models.author import Author
from post.models import Post
from comment.models import Comment
import json

# serializing
from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer

class InboxSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author
    
    def get_items(self, obj):
        item_list = []

        for item in obj.items:
            if item.get('type') == 'post':
                item_list.append(item)
        
        item_list.reverse()
        return item_list
    
    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')

class AllInboxSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_author(self, obj):
        author = AuthorSerializer(obj.author).data
        return author
    
    def get_items(self, obj):
        item_list = []
    
        for item in obj.items:
            item_list.append(item)

        item_list.reverse()
        return item_list
    
    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')

    