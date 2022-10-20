from django.db import models
from datetime import datetime
import uuid

class ContentType(models.TextChoices):
    COMMON_MARK = "text/markdown"
    PLAIN = "text/plain"

class Comment(models.Model):
    type = "comment"
    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    contentType = models.CharField(choices=ContentType.choices, default = ContentType.PLAIN, max_length = 20)
    official_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    published = models.DateTimeField(default=datetime.now)