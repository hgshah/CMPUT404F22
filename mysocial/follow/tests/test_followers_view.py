from django.db import transaction
from django.test import TestCase

from authors.models import Author
from common import TestHelper
from follow.models import Follow


class TestFollowersViewPost(TestCase):
    def setUp(self) -> None:
        self.input_data = {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password': '1234567',
            'display_name': 'user1',
            'github': 'https://github.com/crouton/',
            'host': 'www.crouton.net'
        }

        self.actor = Author.objects.create_user(**self.input_data)
        self.target = Author.objects.create_user(**{
            'username': 'user2',
            'email': 'user2@gmail.com',
            'password': '1234567',
            'display_name': 'user2',
            'github': 'https://github.com/crouton/',
            'host': 'www.crouton.net'
        })

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


class TestFollowersViewGet(TestCase):
    def setUp(self) -> None:
        self.target = TestHelper.create_author('target')
        self.other = TestHelper.create_author('other')
        self.followers = []
        self.non_followers = [self.other]

        for index in range(10):
            oomfie = TestHelper.create_author(f'user{index}')

            # okay, maybe one of them was not accepted yet
            if index == 5:
                self.non_followers.append(oomfie)
                has_accepted = False
            else:
                self.followers.append(oomfie)
                has_accepted = True

            Follow.objects.create(actor=oomfie, target=self.target, has_accepted=has_accepted)

        self.follower_names = map(lambda f: f.display_name, self.followers)
        self.non_follower_names = map(lambda f: f.display_name, self.non_followers)
        self.client.force_login(self.target)

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

