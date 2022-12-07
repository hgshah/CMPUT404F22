from unittest import skip

from authors.util import AuthorUtil
from follow.models import Follow
from follow.tests.base_test_follower_view import BaseTestFollowerView


class TestRequestView(BaseTestFollowerView):
    def setUp(self) -> None:
        super().setUp()
        self.follow = Follow.objects.latest()
        self.path = f'/follows/{self.follow.id}/'

    @skip
    def test_get_successful(self):
        # Either the target or the actor can see this page
        for author_url in (self.follow.actor, self.follow.target):
            author,_ = AuthorUtil.from_author_url_to_author(author_url)
            self.client.logout()
            self.client.force_login(author)
            response = self.client.get(f'/follows/{self.follow.id}/', content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.data)
            self.assertEqual(response.data['id'], str(self.follow.id))

    def test_forbidden(self):
        self.client.logout()
        self.client.force_login(self.followers[5])
        self.follow.has_accepted = False
        self.follow.save()

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
        follow.has_accepted = False
        follow.save()
        self.client.logout()
        self.client.force_login(follow.get_author_target())
        self.path = f'/follows/{follow.id}/'
        response = self.client.put(
            self.path,
            {'hasAccepted': True},
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @skip
    def test_put_forbidden_follower(self):
        # special case: followers cannot accept their own pending request
        self.client.logout()
        author, _ = AuthorUtil.from_author_url_to_author(self.follow.actor)
        self.client.force_login(author)
        response = self.client.put(self.path, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_put_downgrade_error(self):
        for case in ({}, {'hasAccepted': False}):
            response = self.client.put(
                self.path,
                case,
                content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_delete_successful(self):
        follow = Follow.objects.latest()
        path = f'/follows/{follow.id}/'
        response = self.client.delete(path, content_type='application/json')
        self.assertEqual(response.status_code, 204)
