import base64

from django.test import TestCase

from common.test_helper import TestHelper


class TestRemoteNodeView(TestCase):
    def setUp(self) -> None:
        self.local_author = TestHelper.create_author('local_author')
        self.active_node = TestHelper.create_author('active_node', {'author_type': 'active_remote_node'})
        self.inactive_node = TestHelper.create_author('inactive_node', {'author_type': 'inactive_remote_node'})

    class Case:
        def __init__(self, user, result: int):
            self.user = user
            self.result = result

    def test_get_successful(self):
        test_cases = (
            TestRemoteNodeView.Case(None, 401),
            TestRemoteNodeView.Case(self.local_author, 403),
            TestRemoteNodeView.Case(self.active_node, 200),
            TestRemoteNodeView.Case(self.inactive_node, 403),
        )

        for case in test_cases:
            header = {}
            if case.user:
                # from Abhishek Amin at https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/
                token = base64.b64encode(f'{case.user.username}:{TestHelper.DEFAULT_PASSWORD}'.encode('ascii')) \
                    .decode('utf-8')
                header = {
                    'HTTP_AUTHORIZATION': f'Basic {token}'
                }
                print(header)

            response = self.client.get('/remote-node/', **header)
            self.assertEqual(response.status_code, case.result, case.user)
            self.client.logout()
