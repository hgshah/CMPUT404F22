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
            TestRemoteNodeView.Case(None, 404),
            TestRemoteNodeView.Case(self.local_author, 404),
            TestRemoteNodeView.Case(self.active_node, 200),
            TestRemoteNodeView.Case(self.inactive_node, 404),
        )

        for case in test_cases:
            with self.subTest(case=case.user):
                if case.user:
                    self.client.force_login(case.user)

                response = self.client.get('/remote-node/')
                self.assertEqual(response.status_code, case.result)
                self.client.logout()
