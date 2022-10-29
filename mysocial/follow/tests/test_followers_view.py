from django.test import TestCase

from authors.models import Author


class TestFollowersView(TestCase):

    def test_post_successful(self):
        input_data = {
            'username': 'user1',
            'email': 'user1@gmail.com',
            'password': '1234567',
            'display_name': 'user1',
            'github': 'https://github.com/crouton/',
            'host': 'www.crouton.net'
        }
        
        actor = Author.objects.create_user(**input_data)
        target = Author.objects.create_user(**{
            'username': 'user2',
            'email': 'user2@gmail.com',
            'password': '1234567',
            'display_name': 'user2',
            'github': 'https://github.com/crouton/',
            'host': 'www.crouton.net'
        })
        self.client.force_login(actor)
        response = self.client.post(
            f'/authors/{target.official_id}/followers/',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)

        follow = response.data
        self.assertEqual(follow['hasAccepted'], False)
        self.assertEqual(follow['actor']['displayName'], 'user1')
        self.assertEqual(follow['object']['displayName'], 'user2')

