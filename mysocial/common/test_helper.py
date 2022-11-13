from authors.models.author import Author, AuthorType
from post.models import Post, ContentType, Visibility
import datetime
from django.utils import timezone
class TestHelper:
    DEFAULT_PASSWORD = '1234567'

    @staticmethod
    def overwrite_node(username: str, password: str, host: str):
        try:
            node = Author.objects.get(username=username)
            node.set_password(password)
            node.host = host
            node.save()
        except Author.DoesNotExist:
            return TestHelper.create_node(username, password, host)
        except Exception as e:
            print(f"Unknown error: {e}")
            return None

    @staticmethod
    def create_user(username: str, password: str, host: str):
        return TestHelper.create_author(
            username=username,
            other_args={'password': password, 'host': host}
        )

    @staticmethod
    def create_node(username: str, password: str, host: str):
        return TestHelper.create_author(
            username=username,
            other_args={'password': password,
                        'host': host,
                        'author_type': AuthorType.ACTIVE_REMOTE_NODE
                        }
        )

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
            'host': '127.0.0.1:8000',
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
