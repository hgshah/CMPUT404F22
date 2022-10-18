from django.test import TestCase
from django.test import Client

from authors.models import Author


class TestAuthorView(TestCase):
    # todo(turnip): test get_authors, test_get, test_pagination

    def setUp(self) -> None:
        self.client = Client()

    def test_get_author_happy_path(self):
        input_data = {
            "id": 10,
            "username": "user1",
            "email": "user1@gmail.com",
            "password": "1234567",
            "display_name": "display_name",
            "github": "https://github.com/crouton/",
            "host": "www.crouton.net"
        }
        output_data = {
            "id": 10,
            "displayName": "display_name",
            "github": "https://github.com/crouton/"
        }
        Author.objects.create_user(**input_data)
        response = self.client.get(
            f'/{Author.URL_PATH}/10/',
            content_type='application/json',
        )

        assert response.status_code == 200
        for key, value in output_data.items():
            assert value == response.data[key]

    def test_get_author_does_not_exist(self):
        response = self.client.get(
            f'/{Author.URL_PATH}/10/',
            content_type='application/json',
        )

        assert response.status_code == 404

    def test_post_author_happy_path(self):
        response = self.client.post(
            f'/{Author.URL_PATH}/',
            content_type='application/json',
            data={
                "username": "user1",
                "email": "user1@gmail.com",
                "password": "1234567",
                "host": "www.crouton.net"
            }
        )

        assert response.status_code == 200, f"Assertion error: status code: {response.status_code}"
