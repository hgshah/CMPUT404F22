from remote_nodes.node_config_base import NodeConfigBase


class LocalDefault(NodeConfigBase):
    """Base class for all local node configs"""

    domain = '127.0.0.1:8000'
    username = 'local_default'


    @classmethod
    def create_node_credentials(cls):
        return {
            cls.domain: {
                'username': 'local_default',
                'password': 'local_default',
                'remote_username': 'local_default',
                'remote_password': 'local_default',
            }
        }
