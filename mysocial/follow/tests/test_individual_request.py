from follow.models import Follow
from follow.tests.base_test_follower_view import BaseTestFollowerView


class TestRequestView(BaseTestFollowerView):
    def setUp(self) -> None:
        super().setUp()
        self.follow = Follow.objects.latest()
        self.path = f'/follows/{self.follow.id}/'

    def test_get_successful(self):
        # Either the target or the actor can see this page
        for author in (self.follow.actor, self.follow.target):
            self.client.logout()
            self.client.force_login(author)
            response = self.client.get(f'/follows/{self.follow.id}/', content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.data)
            self.assertEqual(response.data['id'], self.follow.id)

    def test_forbidden(self):
        self.client.logout()
        self.client.force_login(self.followers[5])

        response = self.client.get(self.path, content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.client.put(self.path, {'hasAccepted': True}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(self.path, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_does_not_exist(self):
        response = self.client.get('/follows/100/', content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.client.put('/follows/100/', {'hasAccepted': True}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

        response = self.client.delete('/follows/100/', content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_successful(self):
        follow = Follow.objects.latest()
        self.path = f'/follows/{follow.id}/'
        response = self.client.put(
            self.path,
            {'hasAccepted': True},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_forbidden_follower(self):
        # special case: followers cannot accept their own pending request
        self.client.logout()
        self.client.force_login(self.follow.actor)
        response = self.client.put(self.path, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_put_downgrade_error(self):
        for case in ({}, {'hasAccepted': False}):
            response = self.client.put(
                self.path,
                case,
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_delete_successful(self):
        response = self.client.delete(self.path, content_type='application/json')
        self.assertEqual(response.status_code, 204)
