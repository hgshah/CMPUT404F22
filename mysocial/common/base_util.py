from mysocial.settings import base


class BaseUtil:
    """
    Methods and values that are foundational. Could be put in base.py but removed there to prevent clutter

    This file should NOT have many downstream dependencies aka tons of imports above.
    This file has a LOT of upstream dependencies aka a lot of files will depend on this.
    """
    connected_nodes = []

    @staticmethod
    def get_http_or_https() -> str:
        if '127.0.0.1' in base.CURRENT_DOMAIN:
            return 'http://'
        else:
            return 'https://'
