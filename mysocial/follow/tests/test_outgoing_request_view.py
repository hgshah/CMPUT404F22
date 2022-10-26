import unittest
from unittest import skip

from django.test import TestCase


class TestOutgoingRequestView(TestCase):

    @skip("Skip test! Intentionally failing! Not yet done!")
    def test_get_empty(self):
        response = self.client.get(
            '/follows/outgoing/',
            content_type='application/json',
        )

        assert response.status_code == 404


if __name__ == '__main__':
    unittest.main()
