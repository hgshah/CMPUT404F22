import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from mysocial.settings import base
from .author_manager import AuthorManager


class AuthorType(models.TextChoices):
    LOCAL_AUTHOR = "local_author"
    ACTIVE_REMOTE_NODE = "active_remote_node"
    INACTIVE_REMOTE_NODE = "inactive_remote_node"  # we can deactivate nodes by just changing their type


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
    URL_PATH = 'authors'

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

    def get_url(self):
        """
        Returns author_url following the local_author's format
        Example:
            - http://socioecon/authors/{self.official_id}
            - http://{local_host}/authors/{self.official_id}
        """

        return self.get_id()

    def get_id(self):
        """
        Returns author_url following the local_author's format
        Example:
            - http://socioecon/authors/{self.official_id}
            - http://{local_host}/authors/{self.official_id}
        """

        # this is a trick in the serializer for remote authors, look at AuthorSerializer.to_internal_value
        # we are forcing a new field exclusive to remote authors called url, found in Meta.internal_field_equivalents
        if hasattr(self, 'url'):
            return self.url

        # local authors
        return f"http://{base.CURRENT_DOMAIN}/{Author.URL_PATH}/{self.official_id}"

    def is_local(self) -> bool:
        """
        Returns true if the Author object belongs to the local server or current server
        """

        return self.host is None or self.host == '' or self.host == base.CURRENT_DOMAIN

    def get_display_with_domain(self):
        return f'{str(self)}'

    def __str__(self):
        return self.display_name if hasattr(self, 'display_name') and self.display_name else self.username

    @property
    def is_authenticated(self):
        """
        :return: True if the current user is an authenticated local_author or active_remote_node.
        """
        return self.author_type != AuthorType.INACTIVE_REMOTE_NODE and super().is_authenticated

    @property
    def is_authenticated_user(self):
        """
        :return: True if the current user is an authenticated or logged in local_author.
        """
        return self.author_type == AuthorType.LOCAL_AUTHOR and super().is_authenticated

    @property
    def is_authenticated_node(self):
        """
        :return: True if the current user is an authenticated active_remote_node.
        """
        return self.author_type == AuthorType.ACTIVE_REMOTE_NODE and super().is_authenticated

    @staticmethod
    def get_serializer_field_name():
        return "author"

    @classmethod
    def get_author(cls, official_id: str):
        """
        Gets a local author ONLY. Nodes are ignored.
        :param official_id:
        :return: A local_author
        """
        try:
            return cls.objects.get(
                official_id=official_id,
                author_type=AuthorType.LOCAL_AUTHOR
            )
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all_authors(cls):
        """
        Gets all local_author. Nodes are ignored.
        :return: All local_authors.
        """
        return cls.objects.filter(author_type=AuthorType.LOCAL_AUTHOR)
