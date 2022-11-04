from django.db import models
import uuid
from django.utils import timezone

# Create your models here.
class ItemType(models.TextChoices):
    POST = 'post'
    COMMENT = 'comment'
    FOLLOW = 'follow'
    LIKE = 'like'
    UNDEF = 'undef'

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

class InboxPOSTObject(models.Model):
    type = models.CharField(max_length=400, default='undef', blank=False, editable=True)
