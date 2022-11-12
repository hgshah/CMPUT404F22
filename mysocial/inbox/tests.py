from rest_framework.test import APITestCase
from rest_framework import status
from post.models import Post, Visibility
from authors.models.author import Author
from django.utils import timezone
import logging, uuid
import datetime

from common.test_helper import TestHelper

logger = logging.getLogger("mylogger")

# try accessing someone elses inbox
# add a post 200 then GET
# add a comment 200 and it should appear in all
# add a follow request and it should appear in all
# deleting an inbox has empty inbox

class InboxTestCase(APITestCase):
    def setUp(self) -> None:
        self.author1 = TestHelper.create_author(username = "author1")
        TestHelper.create_post()
    
    def test_get_own_inbox_200(self):
        request = f"/authors/{self.author1.official_id}/inbox"

        response = self.client.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    


