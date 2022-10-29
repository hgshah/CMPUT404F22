from django.db import models
from datetime import datetime
import uuid

'''
example like object:
 {
     "@context": "https://www.w3.org/ns/activitystreams",
     "summary": "Lara Croft Likes your post",         
     "type": "Like",
     "author":{
         "type":"author",
         "id":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "host":"http://127.0.0.1:5454/",
         "displayName":"Lara Croft",
         "url":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "github":"http://github.com/laracroft",
         "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
     },
     "object":"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
}
'''
# Create your models here.
class ItemType(models.TextChoices):
    POST = 'post'
    COMMENT = 'comment'
    FOLLOW = 'follow'
    LIKE = 'like'
    MISC = 'misc'
    
class Like(models.Model):
    context = models.CharField(max_length=400)
    summary = models.CharField(max_length=400)
    type = 'like'
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    object = models.CharField(max_length=400)
    # might need dattime

class Inbox(models.Model):
    type = 'inbox'
    author = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    itemType = models.CharField(choices=ItemType.choices, default=ItemType.MISC, max_length=16, blank=False)
    recieved = models.DateTimeField(default=datetime.now())
    content = models.CharField(max_length=800)
