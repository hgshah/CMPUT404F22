# models
from .models import Inbox, InboxPOSTObject
from likes.models import Like
from authors.models import Author
from post.models import Post
from comment.models import Comment

# serializing
from rest_framework import serializers
from post.serializer import PostSerializer 
from authors.serializers.author_serializer import AuthorSerializer
from follow.serializers.follow_serializer import FollowRequestSerializer
from comment.serializers import CommentSerializer, CreateCommentSerializer

'''
{
    "type":"inbox",
    "author":"http://127.0.0.1:5454/authors/c1e3db8ccea4541a0f3d7e5c75feb3fb",
    "items":[
        {
            "type":"post",
            "title":"A Friendly post title about a post about web dev",
            "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "contentType":"text/plain",
            "content":"Þā wæs",
            "author":{
                  "type":"author",
                  "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                  "host":"http://127.0.0.1:5454/",
                  "displayName":"Lara Croft",
                  "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                  "github": "http://github.com/laracroft",
                  "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
            },
            "categories":["web","tutorial"],
            "comments":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments"
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"FRIENDS",
            "unlisted":false
        }, ... { }

class Inbox(models.Model):
    # API fields
    type = 'inbox'
    author = models.UUIDField(primary_key=False, default=0, editable=True)
    item = models.UUIDField(primary_key=False, default=0, editable=True)
    # for backend
    official_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    date_received = models.DateTimeField(default=timezone.now)  # use this to sort list on frontend
    item_type = models.CharField(choices=ItemType.choices, default=ItemType.UNDEF, max_length=16, blank=False)
    ref_like = models.ForeignKey('likes.Like', on_delete=models.CASCADE, blank=True, null=True)
    ref_follow = models.ForeignKey('follow.Follow', on_delete=models.CASCADE, blank=True, null=True)
    ref_post = models.ForeignKey('post.Post', on_delete=models.CASCADE, blank=True, null=True)
    ref_comment = models.ForeignKey('comment.Comment', on_delete=models.CASCADE, blank=True, null=True)

'''

class InboxSerializer(serializers.ModelSerializer):
    type = serializers.CharField()
    author = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        model = Inbox
        fields = ['type', 'author', 'content']

class CreateInboxSerializer(serializers.ModelSerializer):
    def create(self, data):
        inbox_item = Inbox.objects.create(**data)
        return inbox_item

    class Meta:
        model = Inbox
        fields = ['type', 'author', 'item', 'item_type', 'ref_like', 'ref_follow', 'ref_post', 'ref_comment']

class CreatePOSTObjectSerializer(serializers.ModelSerializer):
    def create(self, data):
        item = InboxPOSTObject.objects.create(**data)
        return item
    
    class Meta:
        model = InboxPOSTObject
        fields = ['type']
