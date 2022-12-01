import json

from common.test_helper import TestHelper
from rest_framework import status
from rest_framework.test import APITestCase
from inbox.models import Inbox
from unittest import skip
from post.serializer import PostSerializer
class InboxTestCase(APITestCase):
    CREATE_POST_PAYLOAD = {
        "title": "test",
        "description": "test"
    }

    CREATE_COMMENT_PAYLOAD = {
        "comment": "this is my commment",
        "contentType": "text/plain"
    }

    def setUp(self) -> None:
        self.author1 = TestHelper.create_author(username = "author1")
        self.author2 = TestHelper.create_author(username = "author2")
        self.author2_post = PostSerializer(TestHelper.create_post(author = self.author2)).data

    def test_get_own_inbox(self):
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.official_id}/inbox"

        response = self.client.get(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_add_post_to_inbox(self):
        # add that post to author1's inbox 

        self.client.force_login(self.author1)
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 0)


        request = f"/authors/{self.author1.official_id}/inbox"
        response = self.client.post(request, self.author2_post, format = "json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 1)

    def test_add_comment_to_inbox(self):
        ## create a comment 
        comment = self.create_comment()

        # add that post to author1's inbox 
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 0)

        request = f"{self.author1.get_url()}/inbox"
        response = self.client.post(request, comment, format = "json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 1)

    @skip
    def test_add_follow_to_inbox(self):
        # create follow request 
        follow_request = self.create_follow_request()

        # add that post to author1's inbox 
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 0)

        request = f"/authors/{self.author1.official_id}/inbox"
        response = self.client.post(request, follow_request, format = "json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 1)
    
    @skip
    def test_add_follow_and_comment_appears_in_all(self):
        ## creating and adding comment and follow
        self.add_comment_to_inbox()
        self.add_follow_to_inbox()

        ## Should not appear when we /inbox
        ## Should appear when we inbox/all
        self.client.force_login(self.author1)

        request = f"/authors/{self.author1.official_id}/inbox"
        response = self.client.get(request)
        self.assertEqual(len(response.data["items"]), 0)

        all_request = f"/authors/{self.author1.official_id}/inbox/all"

        response = self.client.get(all_request)
        self.assertEqual(len(response.data["items"]), 2)

    def test_delete_inbox(self):
        ## create a post 
        author2_post = self.create_post()

        # add that post to author1's inbox 
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 0)

        request = f"/authors/{self.author1.official_id}/inbox"
        self.client.post(request, author2_post, format = "json")
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 1)

        # delete inbox
        self.client.force_login(self.author1)
        request = f"/authors/{self.author1.official_id}/inbox"

        self.client.delete(request)
        author1_inbox = Inbox.objects.get(author = self.author1)
        self.assertEqual(len(author1_inbox.items), 0)
    
    @skip
    def test_get_returns_newest(self):
        ## creating and adding comment and follow
        self.add_comment_to_inbox()
        self.add_follow_to_inbox()

        self.client.force_login(self.author1)
        all_request = f"/authors/{self.author1.official_id}/inbox/all"

        response = self.client.get(all_request, type="json")
        self.assertEqual(len(response.data["items"]), 2)

        response_types = []
        for item in response.data["items"]:
            if isinstance(item, str):
                item = json.loads(item)

            response_types.append(item["type"])
        self.assertEqual(response_types, ['Follow', 'comment'])

    def test_get_diff_author_fails(self):
        self.client.force_login(self.author1)
        request = f"/authors/{self.author2.official_id}/inbox/all"

        response = self.client.get(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    '''
    Helper Functions
    '''
    def add_comment_to_inbox(self):
        comment = self.create_comment()
        request = f"/authors/{self.author1.official_id}/inbox"
        self.client.post(request, comment, format = "json")

    def add_follow_to_inbox(self):
        follow_request = self.create_follow_request()
        request = f"/authors/{self.author1.official_id}/inbox"
        self.client.post(request, follow_request, format = "json")

    def create_post(self):
        self.client.force_login(self.author2)
        request = f"/authors/{self.author2.official_id}/posts/"
        return self.client.post(request, self.CREATE_POST_PAYLOAD).data
    
    def create_comment(self):
        self.client.force_login(self.author2)
        base_url = self.author2_post['url']
        request = f'{base_url}/comments'
        response = self.client.post(request, self.CREATE_COMMENT_PAYLOAD)
        return response.data

    def create_follow_request(self):
        self.client.force_login(self.author2)
        return self.client.post(
            f'/authors/{self.author1.official_id}/followers/',
            content_type='application/json',
        ).data




