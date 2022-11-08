from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from authors.models.author import Author
from common.test_helper import TestHelper


class TestAuthor(TestCase):
    def setUp(self) -> None:
        self.local_author = TestHelper.create_author('local_author')
        self.active_node = TestHelper.create_author('active_node', {'author_type': 'active_remote_node'})
        self.inactive_node = TestHelper.create_author('inactive_node', {'author_type': 'inactive_remote_node'})

    class Case:
        def __init__(self, user, result, is_anon=False):
            self.user = user
            self.result = result
            self.is_anon = is_anon

    def test_is_authenticated(self):
        test_cases = (
            TestAuthor.Case(AnonymousUser(), False),
            TestAuthor.Case(self.local_author, True),
            TestAuthor.Case(self.active_node, True),
            TestAuthor.Case(self.inactive_node, False),
        )

        for case in test_cases:
            with self.subTest(case=case.user):
                self.assertEqual(case.user.is_authenticated, case.result)

    def test_is_authenticated_user(self):
        test_cases = (
            TestAuthor.Case(AnonymousUser(), False),
            TestAuthor.Case(self.local_author, True),
            TestAuthor.Case(self.active_node, False),
            TestAuthor.Case(self.inactive_node, False),
        )

        for case in test_cases:
            with self.subTest(case=case.user):
                if not case.user.is_authenticated:
                    self.assertFalse(case.is_anon)
                    continue

                self.assertEqual(case.user.is_authenticated_user, case.result)

    def test_is_authenticated_node(self):
        test_cases = (
            TestAuthor.Case(AnonymousUser(), False),
            TestAuthor.Case(self.local_author, False),
            TestAuthor.Case(self.active_node, True),
            TestAuthor.Case(self.inactive_node, False),
        )

        for case in test_cases:
            with self.subTest(case=case.user):
                if not case.user.is_authenticated:
                    self.assertFalse(case.is_anon)
                    continue

                self.assertEqual(case.user.is_authenticated_node, case.result)

    def test_get_author(self):
        test_cases = (
            TestAuthor.Case(self.local_author, self.local_author),
            TestAuthor.Case(self.active_node, None),
            TestAuthor.Case(self.inactive_node, None),
        )

        for case in test_cases:
            with self.subTest(case=case.user):
                self.assertEqual(Author.get_author(case.user.official_id), case.result)

    def test_get_all_authors(self):
        test_cases = (
            TestAuthor.Case(self.local_author, True),
            TestAuthor.Case(self.active_node, False),
            TestAuthor.Case(self.inactive_node, False),
        )

        authors = Author.get_all_authors()
        self.assertEqual(len(authors), 1)

        for case in test_cases:
            self.assertEqual(case.user in authors, case.result)
