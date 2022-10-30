import unittest

from django.test import TestCase

from common import TestHelper
from follow.models import Follow


class TestPaginationHelper(TestCase):
    # Let's test pagination using one of our views: FollowersView

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

    class Case:
        def __init__(self, page, expected):
            self.page = page
            self.expected_size = expected

    def test_get_successful(self):
        for case in (
                self.Case(1, 4),
                self.Case(2, 4),
                self.Case(3, 1),
        ):
            response = self.client.get(
                f'/authors/{self.target.official_id}/followers/?page={case.page}&size=4',
                content_type='application/json',
            )

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.data)
            self.assertEqual(len(response.data['items']), case.expected_size)
            print(response.data['items'])
            for follower in response.data['items']:
                self.assertIn(follower['displayName'], self.follower_names)
                self.assertNotIn(follower['displayName'], self.non_follower_names)

        # todo
        # fail pagination
        # incomplete
        # negative values
        # out of bounds
