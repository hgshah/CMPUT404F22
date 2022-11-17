from remote_nodes.node_config_base import NodeConfigBase


class UAlberta(NodeConfigBase):
    domain = 'ualberta.herokuapp.com'

    def get_base_url(self):
        return f'https://{self.__class__.domain}'
