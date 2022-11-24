from remote_nodes.node_config_base import NodeConfigBase


class TurnipOomfie(NodeConfigBase):
    domain = 'turnip-oomfie-1.herokuapp.com'
    username = 'turnip'

    def get_base_url(self):
        return f'https://{self.__class__.domain}'
