import pathlib

from django.core.exceptions import ValidationError

from authors.models.author import Author
from authors.serializers.author_serializer import AuthorSerializer
from mysocial.settings import base


# These functions are outside Author to prevent circular dependency and IDEs struggling figuring out type hinting

class AuthorUtil:
    @staticmethod
    def from_author_url_to_author(author_url: str) -> (Author, ValidationError):
        """
        Convert url to Author

        :param author_url:
        :return: Returns a pair of Author and ValidationError

        Example:
            author, err = from_url_to_author(url)

            if err is not None:
                # handle error
                return

            # do logic with author
        """
        serializer = AuthorSerializer(data={'url': author_url})
        if not serializer.is_valid():
            return None, ValidationError(f'{author_url} cannot be deserialized to an Author')

        first_author: Author = serializer.validated_data
        if first_author.is_local():
            # guaranteed complete!
            return first_author, None  # <- GOOD RESULT

        # second pass for remote authors to get the most fields possible
        node_config = base.REMOTE_CONFIG.get(first_author.host)
        if node_config is None:
            return None, ValidationError(f'{author_url} does not have any corresponding domain. domain/host={first_author.host}')

        remote_author = node_config.get_author_via_url(author_url)
        if remote_author is None:
            print('from_author_url_to_author: get_author_via_url returned None')
            return None, ValidationError('from_author_url_to_author: get_author_via_url returned None')

        return remote_author, None

    @staticmethod
    def validate_author_url(author_url: str):
        """
        Do validations only; for Model fields
        :param author_url:
        :return:
        """
        _, err = AuthorUtil.from_author_url_to_author(author_url)
        if err:
            raise err

    @staticmethod
    def from_author_url_to_local_id(local_author_url: str):
        """
        Note: this does NOT validate if the url is not from a local author
        :return:
        """
        return pathlib.PurePath(local_author_url).name
