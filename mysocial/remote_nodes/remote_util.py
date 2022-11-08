from drf_spectacular.utils import OpenApiParameter
from rest_framework.request import Request

from remote_nodes.potato_oomfie import PotatoOomfie
from remote_nodes.turnip_oomfie import TurnipOomfie


class RemoteUtil:
    """
    Remote node configs

    This is where both test and production configurations of each configs are accessible. It's
    a key-value pair of the domain and the corresponding logic of how to call the server and map
    the values into something our internal code can understand.
    """

    REMOTE_NODE_PARAMETERS = [
        OpenApiParameter(name='node', location=OpenApiParameter.QUERY,
                         description='The domain name for the remote node we want to target. For example: '
                                     'node=app.herokuapp.com. We currently support the following nodes:\n'
                                     '- potato-oomfie.herokuapp.com\n '
                                     '- turnip-oomfie-1.herokuapp.com',
                         required=False, type=str),
    ]

    CONFIG: dict = {}

    @staticmethod
    def setup():
        """
        Setup all remote node configs and logic
        """
        for config in (TurnipOomfie, PotatoOomfie):
            RemoteUtil.CONFIG.update(config.create_dictionary_entry())

    @staticmethod
    def extract_node_param(request: Request):
        """
        :param request:
        :return: Either (None, None) if the param does not exist
        or a (string, dict) if it does. Dict here is the request query parameters without the added node
        """
        if 'node' not in request.query_params:
            return None, None
        node_param = request.query_params['node']
        new_dict = request.query_params.copy()
        new_dict.pop('node')
        return node_param, new_dict

    @staticmethod
    def get_node_config(node_param: str):
        if node_param not in RemoteUtil.CONFIG:
            return None
        return RemoteUtil.CONFIG[node_param]
