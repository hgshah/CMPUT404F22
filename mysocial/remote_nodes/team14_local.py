from remote_nodes.local_default import LocalDefault
from remote_nodes.node_config_base import NodeConfigBase


class Team14Local(LocalDefault):
    domain = '127.0.0.1:8014'
    username = 'team14_local'
    remote_fields = {
        'id': 'official_id',
        'url': 'url',
        'display_name': 'display_name',
        'github': 'github',
        'profile_image': 'profile_image'
    }

    def get_base_url(self):
        return f'http://{self.__class__.domain}/api'

    @classmethod
    def create_node_credentials(cls):
        return {
            cls.domain: {
                'username': 'team14_local',
                'password': 'team14_local',
                'remote_username': 'local_default',
                'remote_password': 'local_default',
            }
        }
