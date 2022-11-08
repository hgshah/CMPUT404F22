import json
import os

from remote_nodes.node_config_base import NodeConfigBase


class RemoteConfigs:
    """
    Remote node configs

    This is where both test and production configurations of each configs are accessible. It's
    a key-value pair of the domain and the corresponding logic of how to call the server and map
    the values into something our internal code can understand.
    """
    CONFIG: dict = {}

    @staticmethod
    def setup():
        for config in (NodeConfigBase,):
            RemoteConfigs.CONFIG.update(config.create_dictionary_entry())
