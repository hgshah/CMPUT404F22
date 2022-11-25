from rest_framework.test import APITestCase
from rest_framework import status
from post.models import Post
from common.test_helper import TestHelper
from authors.models.author import Author
from django.utils import timezone
import logging
import datetime

logger = logging.getLogger("mylogger")

class CommentTestCase(APITestCase):
    CREATE_COMMENT_PAYLOAD = {
        "comment": "this is my commment",
        "contentType": "text/plain"
    }

    def setUp(self):
        self.author1 =  TestHelper.create_author(username = "author1", other_args = {"host": "127.0.0.1:8000"})
        self.author2 = TestHelper.create_author(username = "author2", other_args = {"host": "127.0.0.1:8000"})
        self.author1_post = TestHelper.create_post(author = self.author1)
        self.author2_post = TestHelper.create_post(author = self.author2)

    # create a comment on your own post
    def test_create_comment_on_post(self):
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.official_id}/posts/{self.author1_post.official_id}/comments"
       
        response = self.client.post(request, self.CREATE_COMMENT_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.author1.get_id(), response.data["author"]["id"])

    # create a comment on another author's post
    def test_create_comment_on_diff_author_post(self):
        # comment on another authors post
        self.client.force_login(self.author1)
        request = f"/authors/{self.author2.official_id}/posts/{self.author2_post.official_id}/comments"
       
        response = self.client.post(request, self.CREATE_COMMENT_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.author1.get_id(), response.data["author"]["id"])


    # get all comments on a post 
    def test_get_comment_on_post(self):
        # create a comment
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.get_id()}/posts/{self.author1_post.official_id}/comments"
        self.client.post(request, self.CREATE_COMMENT_PAYLOAD)

        # get the post's comments
        response = self.client.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["items"]), 1)





