from unittest import skip

from django.test import TestCase

from common.test_helper import TestHelper
from follow.follow_util import FollowUtil
from follow.models import Follow


class TestFollowUtil(TestCase):
    def setUp(self):
        self.target = TestHelper.overwrite_author('target')
        self.local_follower = TestHelper.overwrite_author('actor')

        # this one is an actual remote author! might break if it disappears!
        # todo: fix later
        self.remote_follower_url = 'https://potato-oomfie.herokuapp.com/authors/7f384aee-8f3f-4326-baad-f0cd372a7662'

    def test_get_followers_local(self):
        # test a local author with a local follower
        Follow.objects.create(actor=self.local_follower.get_url(), target=self.target.get_url(), has_accepted=True)
        followers = FollowUtil.get_followers(self.target)
        self.assertEqual(len(followers), 1)
        self.assertEqual(followers[0], self.local_follower)

    @skip("Broken because of changing how node configurations work")
    def test_get_followers_remote(self):
        # test a local author with a remote follower
        Follow.objects.create(actor=self.remote_follower_url, target=self.target.get_url(), has_accepted=True)
        followers = FollowUtil.get_followers(self.target)
        self.assertEqual(len(followers), 1)
        self.assertEqual(followers[0].get_url(), self.remote_follower_url)

    @skip("Broken because of changing how node configurations work")
    def test_get_followers_mixed(self):
        # test a local author with a mix of local authors and remote authors
        Follow.objects.create(actor=self.local_follower.get_url(), target=self.target.get_url(), has_accepted=True)
        Follow.objects.create(actor=self.remote_follower_url, target=self.target.get_url(), has_accepted=True)
        followers = FollowUtil.get_followers(self.target)
        self.assertEqual(len(followers), 2)
        self.assertEqual(followers[0], self.local_follower)
        self.assertEqual(followers[1].get_url(), self.remote_follower_url)
