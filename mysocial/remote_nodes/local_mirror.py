from remote_nodes.local_default import LocalDefault
from remote_nodes.node_config_base import NodeConfigBase


class LocalMirror(LocalDefault):
    domain = '127.0.0.1:8080'
    username = 'local_mirror'

    @classmethod
    def create_node_credentials(cls):
        return {
            cls.domain: {
                'username': 'local_mirror',
                'password': 'local_mirror',
                'remote_username': 'local_mirror',
                'remote_password': 'local_mirror',
            }
        }
