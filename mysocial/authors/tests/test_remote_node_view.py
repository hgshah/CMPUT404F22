import base64

import requests
from django.test import TestCase

from authors.models.remote_node import NodeStatus
from common.test_helper import TestHelper


class TestRemoteNodeView(TestCase):
    def setUp(self) -> None:
        self.local_author = TestHelper.create_author('local_author')
        self.active_node = TestHelper.create_node('active_node', 'active_node', 'active_node',
                                                  'active_node', 'active_node')
        self.inactive_node = TestHelper.create_node('inactive_node', 'inactive_node', 'inactive_node',
                                                    'inactive_node', 'inactive_node')
        self.inactive_node.node_detail.status = NodeStatus.INACTIVE
        self.inactive_node.node_detail.save()

    class Case:
        def __init__(self, user, result: int):
            self.user = user
            self.result = result

    def test_get_successful(self):
        test_cases = (
            TestRemoteNodeView.Case(None, 401),
            TestRemoteNodeView.Case(self.local_author, 401),
            TestRemoteNodeView.Case(self.active_node, 200),
            TestRemoteNodeView.Case(self.inactive_node, 403),
        )

        for case in test_cases:
            header = {}
            if case.user:
                # from Abhishek Amin at https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/
                token = base64.b64encode(f'{case.user.username}:{case.user.username}'.encode('ascii')) \
                    .decode('utf-8')
                header = {
                    'HTTP_AUTHORIZATION': f'Basic {token}'
                }

            response = self.client.get('/remote-node/', **header)
            self.assertEqual(case.result, response.status_code, case.user)
            self.client.logout()
