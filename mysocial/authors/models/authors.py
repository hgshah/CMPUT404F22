from django.contrib.auth.models import AbstractUser
from .author_manager import AuthorManager


class Author(AbstractUser):
    objects = AuthorManager()
