from authors.models.author import Author, AuthorType


class TestHelper:
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
            'password': '1234567',
            'display_name': '{placeholder}',
            'github': 'https://github.com/{placeholder}/',
            'host': 'www.crouton.net'
        }

        # override
        if other_args is not None:
            default_args.update(other_args)

        # update the unique fields or beneficially unique (like display name)
        for key, value in default_args.items():
            if '{placeholder}' in value:
                default_args[key] = default_args[key].format(placeholder=username)

        return Author.objects.create_user(**default_args)
