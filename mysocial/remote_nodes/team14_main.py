from remote_nodes.node_config_base import NodeConfigBase
from remote_nodes.team14_local import Team14Local


class Team14Main(Team14Local):
    domain = 'social-distribution-14degrees.herokuapp.com'
    username = 'team14'

    def get_base_url(self):
        return f'https://{self.__class__.domain}/api'
