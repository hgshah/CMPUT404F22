from django.test import TestCase


class TestTeam14(TestCase):
    def test_retrieve_all(self):
        response = self.client.get('/authors/?node-target=127.0.0.1:8014')
        self.assertEqual(200, response.status_code)
        print(response.content)

if __name__ == '__main__':
    unittest.main()
