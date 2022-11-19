import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from requests import ConnectionError

from mysocial.settings import base
from .author_manager import AuthorManager
from .remote_node import NodeStatus, RemoteNode


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

    # placed over here to prevent circular dependency
    SERIALIZER = None
    connected_node_classes = ()
    connected_nodes = []

    # Remove this unnecessary fields
    first_name = None
    last_name = None

    """
    Note about official_id: you will never be sure whether this is type UUID or string.
    This depends on the other teams implementation. It may either be string, UUID, or int.
    It's not recommended to directly use this. Use get_id() to make refactoring easier.
    """
    official_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    github = models.TextField(blank=True)
    profile_image = models.ImageField(blank=True)
    node_detail = models.ForeignKey(RemoteNode, on_delete=models.CASCADE, null=True, blank=True)

    objects = AuthorManager()

    REQUIRED_FIELDS = ['email', 'password']

    def is_node(self):
        return self.node_detail is not None

    def is_active_node(self):
        return self.node_detail is not None and self.node_detail.status == NodeStatus.ACTIVE

    def is_inactive_node(self):
        return self.node_detail is not None and self.node_detail.status == NodeStatus.INACTIVE

    def get_url(self):
        """
        Returns url to the exact resource which this Author exists in. This is both for the local author and remote author.

        **This is recommended over using author.url**

        Example:
            - https://socioecon/authors/{self.official_id}
            - https://{local_host}/authors/{self.official_id}
        """

        # this is a trick in the serializer for remote authors, look at AuthorSerializer.to_internal_value
        # we are forcing a new field exclusive to remote authors called url, found in Meta.internal_field_equivalents
        if hasattr(self, 'url'):
            return self.url

        # local authors
        prefix = 'https://'
        if '127.0.0.1' in base.CURRENT_DOMAIN:
            prefix = 'http://'
        return f"{prefix}{base.CURRENT_DOMAIN}/{Author.URL_PATH}/{self.official_id}"

    def get_id(self) -> str:
        """
        Forces UUID to be str. Use this for querying the database or for querying other nodes via NodeConfigBase

        **This is recommended over using author.official_id**
        """
        return str(self.official_id)

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
        return not self.is_inactive_node() and super().is_authenticated

    @property
    def is_authenticated_user(self):
        """
        :return: True if the current user is an authenticated or logged in local_author.
        """
        return not self.is_node() and super().is_authenticated

    @property
    def is_authenticated_node(self):
        """
        :return: True if the current user is an authenticated active_remote_node.
        """
        return self.is_active_node() and super().is_authenticated

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
                node_detail__isnull=True
            )
        except cls.DoesNotExist:
            for node in cls.connected_nodes:
                try:
                    author = node.from_author_id_to_author(official_id)
                except ConnectionError:
                    continue
                except Exception as e:
                    print(f"Author.get_author: Unknown err: {e}")
                    continue

                if author is not None:
                    return author  # <- GODD RESULT HERE
            raise Author.DoesNotExist()
        except Exception as e:
            print(f"Cannot find author {official_id}: {e}")
            return None

    @classmethod
    def get_all_authors(cls):
        """
        Gets all local_author. Nodes are ignored.
        :return: All local_authors.
        """
        return cls.objects.filter(node_detail__isnull=True)
