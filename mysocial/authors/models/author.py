import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .author_manager import AuthorManager
from .author_mixin import AuthorMixin, AuthorType


class Author(AuthorMixin, AbstractUser):
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

    # Remove this unnecessary fields
    first_name = None
    last_name = None

    official_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    github = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True)
    author_type = models.CharField(choices=AuthorType.choices, default=AuthorType.LOCAL_AUTHOR, max_length=25)

    objects = AuthorManager()

    REQUIRED_FIELDS = ['email', 'password']
