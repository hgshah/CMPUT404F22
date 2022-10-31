from unittest import skip
from django.test import TestCase
from django.test import Client

from authors.models import Author


class TestAuthorView(TestCase):
    # todo(turnip): test get_authors, test_get, test_pagination

    def setUp(self) -> None:
        self.client = Client()

    def test_get_author_happy_path(self):
        input_data = {
            "username": "user1",
            "email": "user1@gmail.com",
            "password": "1234567",
            "display_name": "display_name",
            "github": "https://github.com/crouton/",
            "host": "www.crouton.net"
        }
        output_data = {
            "displayName": "display_name",
            "github": "https://github.com/crouton/"
        }
        author = Author.objects.create_user(**input_data)
        output_data['id'] = f"www.crouton.net/authors/{author.official_id}"
        response = self.client.get(
            f'/{Author.URL_PATH}/{author.official_id}/',
            content_type='application/json',
        )

        assert response.status_code == 200, f"Status code: {response.status_code}"
        for key, value in output_data.items():
            assert value == response.data[key]

    def test_get_author_does_not_exist(self):
        response = self.client.get(
            f'/{Author.URL_PATH}/10/',
            content_type='application/json',
        )

        assert response.status_code == 404

    @skip("Skip test! Intentionally failing! Not yet done!")
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
