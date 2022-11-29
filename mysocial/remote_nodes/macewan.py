from remote_nodes.node_config_base import NodeConfigBase


class MacEwan(NodeConfigBase):
    domain = 'macewan.herokuapp.com'
    username = 'macewan'

    def get_base_url(self):
        return f'https://{self.__class__.domain}'
