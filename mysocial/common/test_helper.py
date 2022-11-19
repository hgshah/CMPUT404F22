import datetime

from django.utils import timezone

from authors.models.author import Author
from authors.models.remote_node import RemoteNode
from mysocial.settings import base
from post.models import ContentType, Post, Visibility


class TestHelper:
    DEFAULT_PASSWORD = '1234567'

    @staticmethod
    def overwrite_node(username: str, password: str, remote_username: str, remote_password: str, host: str):
        try:
            node_author = Author.objects.get(username=username)
        except Author.DoesNotExist:
            return TestHelper.create_node(username, password, remote_username, remote_password, host)
        except Exception as e:
            print(f"Unknown error: {e}")
            return None

        node_author.set_password(password)
        node_author.host = host
        node_author.save()

        node_detail = RemoteNode.objects.get(id=node_author.node_detail.id)
        node_detail.remote_username = remote_username
        node_detail.remote_password = remote_password
        node_detail.save()

    @staticmethod
    def create_user(username: str, password: str, host: str):
        return TestHelper.create_author(
            username=username,
            other_args={'password': password, 'host': host}
        )

    @staticmethod
    def create_node(username: str, password: str, remote_username: str, remote_password: str, host: str) -> Author:
        node_author = TestHelper.create_author(
            username=username,
            other_args={'password': password,
                        'host': host,
                        }
        )

        node_detail = RemoteNode.objects.create(remote_username=remote_username, remote_password=remote_password)
        node_author.node_detail = node_detail
        node_author.save()
        return node_author

    @staticmethod
    def overwrite_author(username: str, other_args: dict = None):
        try:
            author = Author.objects.get(username=username)
            for k, v in other_args.items():
                if k == 'password':
                    author.set_password(v)
                else:
                    author.__setattr__(k, v)
            author.save()
            return author
        except Author.DoesNotExist:
            return TestHelper.create_author(username, other_args)
        except Exception as e:
            print(f"Unknown error: {e}")

    @staticmethod
    def create_author(username: str, other_args: dict = None) -> Author:
        """
        Create authors with pre-filled entries based on username
        :param username:
        :param other_args:
        :return:
        """

        default_args = {
            'username': username,
            'email': '{placeholder}@gmail.com',
            'password': TestHelper.DEFAULT_PASSWORD,
            'display_name': '{placeholder}',
            'github': 'https://github.com/{placeholder}/',
            'host': base.CURRENT_DOMAIN,
            'is_staff': False,
        }

        # override
        if other_args is not None:
            default_args.update(other_args)

        # update the unique fields or beneficially unique (like display name)
        for key, value in default_args.items():
            if not isinstance(value, str):
                continue
            if '{placeholder}' in value:
                default_args[key] = default_args[key].format(placeholder=username)

        if 'is_superuser' in default_args:
            return Author.objects.create_superuser(**default_args)
        return Author.objects.create_user(**default_args)

    @staticmethod
    def create_post(author: Author, other_args: dict = None) -> Post:
        default_args = {
            "title": "This is my title",
            "author": author,
            "description": "This is a description",
            "visibility": Visibility.PUBLIC,
            "source": "sourceurl",
            "categories": ["test"],
            "origin": "originURL",
            "contentType": ContentType.PLAIN,
            "unlisted": "False",
            "published": f"{datetime.datetime.now(tz=timezone.utc)}"
        }

        # override
        if other_args is not None:
            default_args.update(other_args)

        return Post.objects.create(**default_args)
