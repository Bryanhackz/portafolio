import unittest

from security import validation


class ValidationTest(unittest.TestCase):
    def test_required_field(self):
        with self.assertRaises(validation.ValidationError) as ctx:
            validation.validate({}, [validation.Field("name", required=True)])
        self.assertIn("name", ctx.exception.errors)

    def test_email_rejected(self):
        with self.assertRaises(validation.ValidationError):
            validation.validate(
                {"email": "no-es-correo"},
                [validation.Field("email", email=True)],
            )

    def test_ok(self):
        out = validation.validate(
            {"name": "Brayan", "email": "b@example.com"},
            [
                validation.Field("name", required=True, min_len=2),
                validation.Field("email", required=True, email=True),
            ],
        )
        self.assertEqual(out["name"], "Brayan")


if __name__ == "__main__":
    unittest.main()