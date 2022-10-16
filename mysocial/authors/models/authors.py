from django.contrib.auth.models import AbstractUser
from mysocial.authors.customauth.author_manager import AuthorManager


class Author(AbstractUser):
    objects = AuthorManager()
