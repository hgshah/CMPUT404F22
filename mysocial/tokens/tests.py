from django.test import TestCase
from rest_framework.authtoken.models import Token

from authors.models.author import Author


class TestObtainCookieAuthToken(TestCase):
    def test_post_successful(self):
        input_data = {
            "username": "user1",
            "email": "user1@gmail.com",
            "password": "1234567",
            "display_name": "display_name",
            "github": "https://github.com/crouton/",
            "host": "www.crouton.net"
        }
        author = Author.objects.create_user(**input_data)
        response = self.client.post(
            f'/tokens/',
            {"username": "user1", "password": "1234567"},
            content_type='application/json')
        token, _ = Token.objects.get_or_create(user=author)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], str(token))
