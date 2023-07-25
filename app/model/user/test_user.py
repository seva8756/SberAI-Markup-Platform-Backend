import unittest

from app.model import TestUser


class UserTest(unittest.TestCase):
    def test_Validate(self):
        def valid():
            return TestUser()

        def with_encrypted_password():
            u = TestUser()
            u.password = ""
            u.encrypted_password = "encryptedpassword"
            return u

        def empty_email():
            u = TestUser()
            u.email = ""
            return u

        def invalid_email():
            u = TestUser()
            u.email = "invalid"
            return u

        def empty_password():
            u = TestUser()
            u.password = ""
            return u

        def short_password():
            u = TestUser()
            u.password = "short"
            return u

        def empty_firstname():
            u = TestUser()
            u.first_name = ""
            return u

        def empty_lastname():
            u = TestUser()
            u.last_name = ""
            return u

        testCases = (
            {
                "name": "valid",
                "u": valid,
                "isValid": True
            },
            {
                "name": "with encrypted password",
                "u": with_encrypted_password,
                "isValid": True
            },
            {
                "name": "empty email",
                "u": empty_email,
                "isValid": False
            },
            {
                "name": "invalid email",
                "u": invalid_email,
                "isValid": False
            },
            {
                "name": "empty password",
                "u": empty_password,
                "isValid": False
            },
            {
                "name": "short password",
                "u": short_password,
                "isValid": False
            },
            {
                "name": "empty firstname",
                "u": empty_firstname,
                "isValid": False
            },
            {
                "name": "empty lastname",
                "u": empty_lastname,
                "isValid": False
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                res, err = val["u"]().Validate()
                if val["isValid"]:
                    self.assertTrue(res, msg=err)
                else:
                    self.assertFalse(res, msg=err)

    def test_BeforeCreate(self):
        u = TestUser()
        self.assertIsNone(u.BeforeCreate())
        self.assertNotEqual(u.encrypted_password, "")


if __name__ == '__main__':
    unittest.main()
