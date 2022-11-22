from remote_nodes.node_config_base import NodeConfigBase


class PotatoOomfie(NodeConfigBase):
    domain = 'potato-oomfie.herokuapp.com'

    def get_base_url(self):
        return f'https://{self.__class__.domain}'
