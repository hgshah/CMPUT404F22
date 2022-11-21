from remote_nodes.node_config_base import NodeConfigBase


class Socioecon(NodeConfigBase):
    domain = 'socioecon.herokuapp.com'
    username = 'socioecon'

    def get_base_url(self):
        return f'https://{self.__class__.domain}'
