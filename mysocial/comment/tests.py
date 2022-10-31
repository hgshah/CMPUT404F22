from rest_framework.test import APITestCase
from rest_framework import status
from post.models import Post
from comment.models import Comment, ContentType
from authors.models import Author
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
        author1_data = {
            "username": "user1",
            "email": "user1@gmail.com",
            "password": "1234567",
            "display_name": "display_name",
            "github": "https://github.com/crouton/",
            "host": "www.crouton.net"
        }
        author2_data = {
            "username": "user2",
            "email": "user2@gmail.com",
            "password": "1234567",
            "display_name": "display_name",
            "host": "www.crouton.net"
        }
        self.author1 = Author.objects.create_user(**author1_data)
        self.author2 = Author.objects.create_user(**author2_data)
        self.author1_post = Post.objects.create(author = self.author1, title = "test", description = "test", published = datetime.datetime.now(tz=timezone.utc))
        self.author2_post = Post.objects.create(author = self.author2, title = "test2", description = "test2", published = datetime.datetime.now(tz=timezone.utc))

    # create a comment on your own post
    def test_create_comment_on_post(self):
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.official_id}/posts/{self.author1_post.official_id}/comments"
       
        response = self.client.post(request, self.CREATE_COMMENT_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.author1.official_id) in response.data["author"]["id"])

    # create a comment on another author's post
    def test_create_comment_on_diff_author_post(self):
        # comment on another authors post
        self.client.force_login(self.author1)
        request = f"/authors/{self.author2.official_id}/posts/{self.author2_post.official_id}/comments"
       
        response = self.client.post(request, self.CREATE_COMMENT_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.author1.official_id) in response.data["author"]["id"])


    # get all comments on a post 
    def test_get_comment_on_post(self):
        # create a comment
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.official_id}/posts/{self.author1_post.official_id}/comments"
        self.client.post(request, self.CREATE_COMMENT_PAYLOAD)

        # get the post's comments
        response = self.client.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["items"]), 1)





