import requests
from django.utils.baseconv import base64

from mysocial.settings import base


class NodeConfigBase:
    """
    Sample and base config

    Remember to call super whenever possible; use good judgment to determine when to call super in the method body.
    """

    # todo(turnip): check entry in Author, if does not exist, make one

    """
    Call domain with self.__class__.domain so you can override it in classes that inherit this.
    Inheriting classes may not need it unless when needed
    """
    domain = 'domain.herokuapp.com'

    def __init__(self):
        if base.CURRENT_DOMAIN == '127.0.0.1:8000':
            self.username = 'username'
            self.password = 'password'
            return

        credentials = base.REMOTE_CONFIG_CREDENTIALS[self.__class__.domain]
        self.username = credentials['username']
        self.password = credentials['password']
        # todo(turnip): check entry in Author, check if inactive?

    @classmethod
    def create_dictionary_entry(cls):
        return {cls.domain: NodeConfigBase()}

    def get_author(self, author_url: str):
        token = base64.b64encode(f'{self.username}:{self.password}'.encode('ascii')).decode('utf-8')
        headers = {'HTTP_AUTHORIZATION': f'Basic {token}'}
        response = requests.get(author_url, **headers)

        if response.status_code == 200:
            # todo(turnip): map to our author?
            return response.data
        else:
            return None
