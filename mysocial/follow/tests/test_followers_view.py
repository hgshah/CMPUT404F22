from django.db import transaction
from django.test import TestCase

from common import TestHelper
from follow.models import Follow
from follow.tests.base_test_follower_view import BaseTestFollowerView


class TestFollowersViewPost(TestCase):
    def setUp(self) -> None:
        self.actor = TestHelper.create_author('user1')
        self.target = TestHelper.create_author('user2')

    def test_post_successful(self):
        self.client.force_login(self.actor)
        response = self.client.post(
            f'/authors/{self.target.official_id}/followers/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)

        follow = response.data
        self.assertEqual(follow['hasAccepted'], False)
        self.assertEqual(follow['actor']['displayName'], 'user1')
        self.assertEqual(follow['object']['displayName'], 'user2')

    def test_post_unauthenticated(self):
        response = self.client.post(
            f'/authors/{self.target.official_id}/followers/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 404)

    def test_post_follow_self(self):
        self.client.force_login(self.actor)
        response = self.client.post(
            f'/authors/{self.actor.official_id}/followers/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)

    def test_post_author_does_not_exist(self):
        self.client.force_login(self.actor)
        response = self.client.post(
            f'/authors/00000000-00000000-00000000-00000000/followers/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 404)

    def test_post_already_following(self):
        self.client.force_login(self.actor)

        for test_value in (True, False):
            with transaction.atomic():  # need because we're intentionally causing an error here
                f = Follow.objects.create(actor=self.actor, target=self.target, has_accepted=test_value)
                response = self.client.post(
                    f'/authors/{self.target.official_id}/followers/',
                    content_type='application/json',
                )
                self.assertEqual(response.status_code, 400)
            f.delete()


class TestFollowersViewGet(BaseTestFollowerView):
    def setUp(self) -> None:
        super().setUp()

    def test_get_successful(self):
        response = self.client.get(
            f'/authors/{self.target.official_id}/followers/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data['items']), 9)
        for follower in response.data['items']:
            self.assertIn(follower['displayName'], self.follower_names)
            self.assertNotIn(follower['displayName'], self.non_follower_names)

    def test_get_author_does_not_exist(self):
        response = self.client.get(
            f'/authors/00000000-00000000-00000000-00000000/followers/',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_pagination_fails(self):
        response = self.client.get(
            f'/authors/{self.target.official_id}/followers/?page=-1&size=2',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)
