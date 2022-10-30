import unittest

from django.test import TestCase

from common import TestHelper
from follow.models import Follow


class TestPaginationHelper(TestCase):
    # Let's test pagination using one of our views: FollowersView

    class Case:
        def __init__(self, page, expected=4, size=4):
            self.page = page
            self.size = size
            self.expected_size = expected

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

        self.follower_names = list(map(lambda f: f.display_name, self.followers))
        self.non_follower_names = list(map(lambda f: f.display_name, self.non_followers))
        self.client.force_login(self.target)
        self.Case = TestPaginationHelper.Case

    def test_get_successful_no_pagination(self):
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

    def test_get_successful(self):
        for case in (
                self.Case(1, 4),  # edge at the beginning
                self.Case(2, 4),
                self.Case(3, 1),  # edge at the end
                self.Case(1, 9, size=10),  # big page
        ):
            response = self.client.get(
                f'/authors/{self.target.official_id}/followers/?page={case.page}&size={case.size}',
                content_type='application/json',
            )

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.data)
            self.assertEqual(len(response.data['items']), case.expected_size)
            for follower in response.data['items']:
                self.assertIn(follower['displayName'], self.follower_names)
                self.assertNotIn(follower['displayName'], self.non_follower_names)

    def test_get_fail_general(self):
        for case in (
                self.Case('a'),
                self.Case(-1),
                self.Case(2, size=9),  # edge at the end
                self.Case(4, size=4),  # edge at the end
        ):
            response = self.client.get(
                f'/authors/{self.target.official_id}/followers/?page={case.page}&size={case.size}',
                content_type='application/json',
            )

            self.assertEqual(response.status_code, 404)

    def test_get_fail_missing_param(self):
        # missing page
        response = self.client.get(
            f'/authors/{self.target.official_id}/followers/?size=4',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

        # missing size
        response = self.client.get(
            f'/authors/{self.target.official_id}/followers/?page=1',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)
