from rest_framework import serializers
from authors.serializers.author_serializer import AuthorSerializer
from drf_spectacular.utils import extend_schema_field
from likes.models import Like

class LikeSerializer(serializers.ModelSerializer):
    summary = serializers.SerializerMethodField()
    
    def get_summary(self, obj):
        print(obj.author)
        display_name = obj.author.get('displayName')
        return f'{display_name} Likes your post'
    class Meta:
        model = Like
        fields = ('summary', 'author', 'type', 'object')
