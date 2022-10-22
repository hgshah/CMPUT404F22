import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .author_manager import AuthorManager


class Author(AbstractUser):
    """
    Fields:
    - Inherited fields not shown below:
        :ivar id: auto generated BigInt
        :ivar password: str; encrypted
        :ivar last_login: datetime
        :ivar is_superuser: bool
        :ivar username: str; unique constraint
        :ivar email: str; unique constraint
        :ivar is_staff: bool
        :ivar is_active: bool
        :ivar date_joined: datetime

    from: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    URL_PATH = "authors"

    # Remove this unnecessary fields
    first_name = None
    last_name = None

    official_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.TextField()
    display_name = models.TextField(blank=True)
    github = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True)

    objects = AuthorManager()

    REQUIRED_FIELDS = ['email', 'host', 'password']

    @staticmethod
    def get_serializer_field_name():
        return "author"

    def __str__(self):
        return self.display_name if self.display_name else self.username


