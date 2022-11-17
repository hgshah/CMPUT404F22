from remote_nodes.node_config_base import NodeConfigBase
from remote_nodes.team14_local import Team14Local


class Team14Main(Team14Local):
    domain = 'team14.herokuapp.com'

    def get_base_url(self):
        return f'http://{self.__class__.domain}/api'
