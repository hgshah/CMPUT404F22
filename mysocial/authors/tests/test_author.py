from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from common.test_helper import TestHelper


class TestAuthor(TestCase):
    def setUp(self) -> None:
        self.local_author = TestHelper.create_author('local_author')
        self.active_node = TestHelper.create_author('active_node', {'author_type': 'active_remote_node'})
        self.inactive_node = TestHelper.create_author('inactive_node', {'author_type': 'inactive_remote_node'})

    class Case:
        def __init__(self, user, result: bool, is_anon=False):
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
