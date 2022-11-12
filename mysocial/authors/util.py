import pathlib
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

from authors.models.author import Author
from mysocial.settings import base


# These functions are outside Author to prevent circular dependency and IDEs struggling figuring out type hinting

class AuthorUtil:
    @staticmethod
    def from_author_url_to_author(author_url: str) -> (Author, ValidationError):
        """
        Convert url to Author

        :param author_url:
        :return: Returns a pair of Author and ValidationError

        Note: this is still not on par with what I want. It may either return an Author or the dictionary form of
        an Author. I want to hopefully make this something like an Author, whether remote or local

        Example:
            author, err = from_url_to_author(url)

            if err is not None:
                # handle error
                return

            # do logic with author
        """
        # by Philipp Claßen from https://stackoverflow.com/a/56476496/17836168
        _, domain, path, _, _, _ = urlparse(author_url)

        if domain == base.CURRENT_DOMAIN:
            local_id = AuthorUtil.from_author_url_to_local_id(path)
            author = Author.get_author(official_id=local_id)
            err = None
            if author is None:
                err = ValidationError(f'There is no local_author with id {path.name}')
            return author, err

        # check if we have this server
        node_config = base.REMOTE_CONFIG.get(domain)
        if node_config is None:
            return None, ValidationError(f'{author_url} does not have any corresponding domain')

        author = node_config.get_author_via_url(author_url)
        if author is None:
            return None, ValidationError(f'{author_url} does not exist in the domain {domain}')
        return author, None

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
