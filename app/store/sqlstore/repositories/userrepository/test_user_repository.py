import unittest

from app.store.errors import ErrRecordNotFound

from app.model import TestUser
from app.store.sqlstore.testing import TestDB
from app.store.sqlstore import Store


class UserRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_Create(self):
        try:
            db, teardown = TestDB()
            s = Store(db)
            u = TestUser()
            err = s.User().Create(u)
            self.assertIsNone(err)
            self.assertTrue(hasattr(u, "ID"))
        finally:
            teardown("users")

    def test_FindByEmail(self):
        try:
            db, teardown = TestDB()
            s = Store(db)
            u1 = TestUser()
            _, err = s.User().FindByEmail(u1.email)
            self.assertEqual(err, ErrRecordNotFound)

            s.User().Create(u1)
            u2, err = s.User().FindByEmail(u1.email)
            self.assertIsNone(err)
            self.assertIsNotNone(u2)
        finally:
            teardown("users")

    def test_Find(self):
        try:
            db, teardown = TestDB()
            s = Store(db)
            u1 = TestUser()
            _, err = s.User().Find(0)
            self.assertEqual(err, ErrRecordNotFound)

            s.User().Create(u1)
            u2, err = s.User().Find(u1.ID)
            self.assertIsNone(err)
            self.assertIsNotNone(u2)
        finally:
            teardown("users")


if __name__ == '__main__':
    unittest.main()
