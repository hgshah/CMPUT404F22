import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    """from https://stackoverflow.com/a/48159596/17836168"""
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)