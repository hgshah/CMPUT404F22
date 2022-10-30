from django.test import TestCase

from common import TestHelper
from follow.models import Follow


class BaseTestFollowerView(TestCase):
    def setUp(self) -> None:
        self.target = TestHelper.create_author('target')
        self.other = TestHelper.create_author('other')
        self.followers = []
        self.non_followers = [self.other]
        self.pending = []

        for index in range(10):
            oomfie = TestHelper.create_author(f'user{index}')

            # okay, maybe one of them was not accepted yet
            if index == 5:
                self.non_followers.append(oomfie)
                self.pending.append(oomfie)
                has_accepted = False
            else:
                self.followers.append(oomfie)
                has_accepted = True

            Follow.objects.create(actor=oomfie, target=self.target, has_accepted=has_accepted)

        self.follower_names = map(lambda f: f.display_name, self.followers)
        self.non_follower_names = map(lambda f: f.display_name, self.non_followers)
        self.client.force_login(self.target)
