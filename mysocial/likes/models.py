from django.db import models
# Create your models here.

class LikeType(models.TextChoices):
    POST = "post"
    COMMENT = "comment"

class Like(models.Model):
    type = "Like"
    author = models.JSONField() 
    author_id = models.TextField()
    object = models.TextField()
    object_type = models.CharField(choices = LikeType.choices, max_length= 20)
    class Meta:
        unique_together = ('author_id', 'object')

