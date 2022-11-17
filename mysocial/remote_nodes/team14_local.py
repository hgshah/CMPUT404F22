from remote_nodes.node_config_base import NodeConfigBase


class Team14Local(NodeConfigBase):
    domain = '127.0.0.1:8014'

    def get_base_url(self):
        return f'http://{self.__class__.domain}/api'







