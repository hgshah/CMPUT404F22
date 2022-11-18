import json

from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class ItemType(models.TextChoices):
    POST = 'post'
    COMMENT = 'comment'
    FOLLOW = 'follow'
    LIKE = 'like'

class Inbox(models.Model):
    type = 'inbox'
    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)
    official_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    items = ArrayField(models.JSONField(), blank = True, default = list)

    def add_to_inbox(self, data):
        # todo: create UUID serializer; serializer can't parse UUID; check out
        #  https://stackoverflow.com/a/48159596/17836168
        self.items.append(json.dumps(data))
        self.save()
