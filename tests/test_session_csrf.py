import unittest

import config
from security import csrf, session


class SessionTest(unittest.TestCase):
    def setUp(self):
        self._original_secret = config.SECRET_KEY
        config.SECRET_KEY = "test-secret"

    def tearDown(self):
        config.SECRET_KEY = self._original_secret

    def test_roundtrip(self):
        token = session.create_token(42)
        payload = session.verify_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["uid"], 42)

    def test_tampered_token(self):
        token = session.create_token(42)
        self.assertIsNone(session.verify_token(token + "x"))

    def test_expired_token(self):
        from unittest.mock import patch
        token = session.create_token(42)
        with patch("security.session.time.time", return_value=10**18):
            self.assertIsNone(session.verify_token(token))

    def test_csrf_matches(self):
        token = csrf.new_token()
        self.assertTrue(csrf.token_matches(token, token))
        self.assertFalse(csrf.token_matches(token, token + "x"))

    def test_csrf_rejects_unsigned(self):
        # Un atacante no puede fabricar un token válido sin SECRET_KEY
        self.assertFalse(csrf.token_matches("evil", "evil"))
        self.assertFalse(csrf.token_matches("evil.sig", "evil.sig"))


if __name__ == "__main__":
    unittest.main()