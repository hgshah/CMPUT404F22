from mysocial.settings import base


class BaseUtil:
    """
    functions related to base.py but we don't want to put it in base.py

    prevents circular dependency
    """

    @staticmethod
    def get_http_or_https() -> str:
        if '127.0.0.1' in base.CURRENT_DOMAIN:
            return 'http://'
        else:
            return 'https://'
