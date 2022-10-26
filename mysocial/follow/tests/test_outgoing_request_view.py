import unittest
from django.test import TestCase
from django.test import Client


class TestOutgoingRequestView(TestCase):
    def test_get_empty(self):
        response = self.client.get(
            '/follows/outgoing/',
            content_type='application/json',
        )

        assert response.status_code == 404


if __name__ == '__main__':
    unittest.main()
