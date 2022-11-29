from django.test import TestCase

from authors.models.author import Author
from common.base_util import BaseUtil
from common.test_helper import TestHelper
from mysocial.settings import base


class TestAuthorView(TestCase):
    def setUp(self) -> None:
        for author in Author.objects.all():
            author.delete()
        BaseUtil.connected_nodes = ()  # remove all nodes

        self.users = []
        for index in range(10):
            self.users.append(TestHelper.create_author(f'user{index}'))

    def test_get_author_happy_path(self):
        user = self.users[4]
        response = self.client.get(
            f'/{Author.URL_PATH}/{user.official_id}/',
            content_type='application/json',
        )
        output_data = {
            "type": "author",
            "id": user.get_id(),
            "url": f"http://{base.CURRENT_DOMAIN}/authors/{user.official_id}",
            "host": user.host,
            "displayName": user.display_name,
            "github": user.github,
            "profileImage": user.profile_image,
        }

        self.assertEqual(response.status_code, 200)
        for key, value in output_data.items():
            self.assertEqual(response.data[key], value)

    def test_get_all_author_happy_path(self):
        response = self.client.get(
            f'/{Author.URL_PATH}/',
        )

        self.assertEqual(response.status_code, 200)
        output_users = response.data['items']
        self.assertEqual(len(output_users), len(self.users))
        for index in range(len(output_users)):
            actual_user = output_users[index]
            expected_user = self.users[index]
            self.assertEqual(actual_user['github'], expected_user.github)
            self.assertEqual(actual_user['displayName'], expected_user.display_name)

    def test_get_all_authors_failed_pagination(self):
        response = self.client.get(
            f'/{Author.URL_PATH}/?size=-1',
        )

        self.assertEqual(response.status_code, 404)

    def test_get_author_does_not_exist(self):
        response = self.client.get(
            f'/{Author.URL_PATH}/10/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 404)
