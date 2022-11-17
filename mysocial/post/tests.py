from rest_framework.test import APITestCase
from rest_framework import status
from post.models import Post, Visibility
from authors.models.author import Author
from django.utils import timezone
import logging, uuid
import datetime
from common.test_helper import TestHelper
from inbox.models import Inbox 

logger = logging.getLogger("mylogger")
#pymike00, October 29, https://www.youtube.com/watch?v=1FqxfnlQPi8&ab_channel=pymike00

#mg22, October 29, https://stackoverflow.com/questions/44604686/how-to-test-a-model-that-has-a-foreign-key-in-django
#kravietz, October 29, https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
class PostTestCase(APITestCase):
    CREATE_POST_PAYLOAD = {
    "title": "test",
    "description": "test"
    }
    
    def setUp(self) -> None:
        self.author1 =  TestHelper.create_author(username = "author1", other_args = {"host": "127.0.0.1:8000"})
        self.author2 = TestHelper.create_author(username = "author2", other_args = {"host": "127.0.0.1:8000"})
        self.existing_post = TestHelper.create_post(author = self.author1)
        self.private_post = TestHelper.create_post(author = self.author1, other_args = {"visibility": Visibility.FRIENDS}) 
        self.author2_post = TestHelper.create_post(author = self.author2)

    # GET posts/public
    def test_get_all_public_posts(self):
        request = "/posts/public/"

        response = self.client.get(request)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # GET /authors/{AUTHOR_UUID}/posts?page={INT}&size={INT}
    def test_get_posts_by_author(self):
        # author 1 should have 2 created posts
        request = f"/authors/{self.author1.official_id}/posts/?page={1}&size={2}"

        response = self.client.get(request)

        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # author 2 should have 1 created post
        request = f"/authors/{self.author2.official_id}/posts/?page={1}&size={2}"

        response = self.client.get(request)

        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # POST /authors/{AUTHOR_UUID}/posts/
    def test_create_post(self):
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.official_id}/posts/"

        response = self.client.post(request, self.CREATE_POST_PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(str(self.author1.official_id) in response.data["author"]["id"])

    # GET /authors/{AUTHOR_UUID}/posts/{POST_UUID}
    def test_get_specific_post(self):
        request = f"/authors/{self.author1.official_id}/posts/{self.existing_post.official_id}/"

        response = self.client.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # DELETE /authors/{AUTHOR_UUID}/posts/{POST_UUID}
    def test_delete_post(self):
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.official_id}/posts/{self.existing_post.official_id}/"

        response = self.client.delete(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    #POST /authors/{AUTHOR_UUID}/posts/{POST_UUID}
    def test_update_post(self):
        self.client.force_login(self.author1)
        new_data = {"title": "new title", "description": "new description"}
        request = f"/authors/{self.author1.official_id}/posts/{self.existing_post.official_id}/"
        
        response = self.client.put(request, new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], new_data["title"])
        self.assertEqual(response.data["description"], new_data["description"])

    #PUT /authors/{AUTHOR_UUID}/posts/{POST_UUID}
    def test_update_or_create_post(self):
        self.client.force_login(self.author1)
        new_uuid = uuid.uuid4()
        request = f"/authors/{self.author1.official_id}/posts/{new_uuid}/"

        response = self.client.put(request, self.CREATE_POST_PAYLOAD)

        self.assertEqual(response.data["id"], self.get_expected_official_id(new_uuid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def get_expected_official_id(self, post_id):
        return f"http://{self.author1.host}/{Author.URL_PATH}/{self.author1.official_id}/posts/{post_id}"

class PostFailTestCase(APITestCase):
    CREATE_POST_PAYLOAD = {
        "title": "test",
        "description": "test"
        }
    
    def setUp(self) -> None:
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
        self.existing_post = TestHelper.create_post(author = self.author1) 

    # Updating a post as a different user
    def test_modify_as_different_user(self):
        self.client.force_login(self.author2)
        new_data = {"title": "new title", "description": "new description"}
        request = f"/authors/{self.author1.official_id}/posts/{self.existing_post.official_id}/"
        
        response = self.client.put(request, new_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # Deleting a post as a different user
    def test_delete_as_different_user(self):
        self.client.force_login(self.author2)
        request = f"/authors/{self.author1.official_id}/posts/{self.existing_post.official_id}/"

        response = self.client.delete(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)






    

    
    



    
    


    



