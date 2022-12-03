from django.db import models
from datetime import datetime
import uuid
from django.contrib.postgres.fields import ArrayField


# AMANDA TO DO:
#count
#comments
#commentsSrc
# categories --> we need to switch to a postgres db lol
class Visibility(models.TextChoices):
    FRIENDS = "friends"
    PUBLIC = "public"

class ContentType(models.TextChoices):
    COMMON_MARK = "text/markdown"
    PLAIN = "text/plain"
    APPLICATION = "application/base64"
    EMBEDDED_PNG = "image/png;base64"
    EMBEDDED_JPEG = "image/jpeg;base64"

class Post(models.Model):
    type = "post"
    official_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    title = models.CharField(max_length=500, blank = True)
    source = models.CharField(max_length=500, default = "www.default.com")
    origin = models.CharField(max_length=500, default = "www.default.com")
    categories = ArrayField(models.CharField(max_length = 30), default=list)
    published = models.DateTimeField(default=datetime.now)
    description = models.CharField(max_length=500, blank = True)
    content = models.TextField(default = "", blank = True)
    unlisted = models.BooleanField(default=False)

    # comments
    count = models.PositiveIntegerField(default = 0, blank = True)

    author = models.ForeignKey('authors.Author', on_delete = models.CASCADE)

    visibility = models.CharField(choices = Visibility.choices, default = Visibility.PUBLIC, max_length = 20)
    contentType = models.CharField(choices=ContentType.choices, default = ContentType.PLAIN, max_length = 20)

    def get_id(self) -> str:
        return str(self.official_id)

    def get_url(self) -> str:
        # note: we might have to refactor this if some other team has a funky posts url
        author_url = self.author.get_url().rstrip('/')
        return f'{author_url}/posts/{self.official_id}'

    def get_comments_url(self) -> str:
        # note: we might have to refactor this if some other team has a funky comments url
        author_url = self.author.get_url().rstrip('/')
        return f'{author_url}/posts/{self.official_id}/comments'
