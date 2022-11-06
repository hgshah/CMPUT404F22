from follow.tests.base_test_follower_view import BaseTestFollowerView


class TestRequestView(BaseTestFollowerView):
    def setUp(self) -> None:
        super().setUp()

    def test_get_successful_incoming(self):
        response = self.client.get(
            '/follows/incoming/',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data['items']), len(self.pending))

    def test_get_successful_outgoing(self):
        # login as that one user who's waiting to get accepted
        self.client.logout()
        self.client.force_login(self.pending[0])

        response = self.client.get(
            '/follows/outgoing/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data['items']), 1)

    def test_get_unauthenticated(self):
        self.client.logout()
        for case in ('/follows/incoming/', '/follows/outgoing/'):
            response = self.client.get(
                case,
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 401)

    def test_get_fail_pagination(self):
        for case in ('/follows/incoming/?page=1', '/follows/outgoing/?page=1'):
            response = self.client.get(
                case,
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 404)
