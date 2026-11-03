import unittest

from data import authorizer


class AuthorizerTest(unittest.TestCase):
    def test_anonymous_cannot_write(self):
        self.assertFalse(authorizer.can_write_project(None))

    def test_admin_can_write(self):
        self.assertTrue(authorizer.can_write_project({"user_id": 1, "role": "admin"}))

    def test_public_read_of_published(self):
        self.assertTrue(authorizer.can_read_project(None, {"published": 1}))

    def test_anonymous_cannot_read_draft(self):
        self.assertFalse(authorizer.can_read_project(None, {"published": 0}))


if __name__ == "__main__":
    unittest.main()