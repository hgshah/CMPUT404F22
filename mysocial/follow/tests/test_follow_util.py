from django.test import TestCase

from common.test_helper import TestHelper
from follow.follow_util import FollowUtil
from follow.models import Follow


class TestFollowUtil(TestCase):
    def setUp(self):
        self.target = TestHelper.create_author('target')
        self.local_follower = TestHelper.create_author('actor')

        # this one is an actual remote author! might break if it disappears!
        self.remote_follower_url = 'http://potato-oomfie.herokuapp.com/authors/7a50a4b3-7a0b-4891-ab3e-da51c9119443'

    def test_get_followers_local(self):
        # test a local author with a local follower
        Follow.objects.create(actor=self.local_follower.get_url(), target=self.target.get_url(), has_accepted=True)
        followers = FollowUtil.get_followers(self.target)
        self.assertEqual(len(followers), 1)
        self.assertEqual(followers[0], self.local_follower)

    def test_get_followers_remote(self):
        # test a local author with a remote follower
        Follow.objects.create(actor=self.remote_follower_url, target=self.target.get_url(), has_accepted=True)
        followers = FollowUtil.get_followers(self.target)
        self.assertEqual(len(followers), 1)
        self.assertEqual(followers[0].get_url(), self.remote_follower_url)

    def test_get_followers_mixed(self):
        # test a local author with a mix of local authors and remote authors
        Follow.objects.create(actor=self.local_follower.get_url(), target=self.target.get_url(), has_accepted=True)
        Follow.objects.create(actor=self.remote_follower_url, target=self.target.get_url(), has_accepted=True)
        followers = FollowUtil.get_followers(self.target)
        self.assertEqual(len(followers), 2)
        self.assertEqual(followers[0], self.local_follower)
        self.assertEqual(followers[1].get_url(), self.remote_follower_url)
