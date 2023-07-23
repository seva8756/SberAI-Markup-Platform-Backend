import unittest

from app.store.errors import ErrRecordNotFound
from app.store.sqlstore.test_store import (
    database_config,
    MainTest
)

from app.model import TestUser
from app.store.sqlstore.testing import TestDB
from app.store.sqlstore import Store


class UserRepositoryTest(MainTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_Create(self):
        try:
            db, teardown = TestDB(database_config)
            s = Store(db)
            u = TestUser()
            err = s.User().Create(u)
            self.assertIsNone(err)
            self.assertTrue(hasattr(u, "ID"))
        finally:
            teardown("users")

    def test_FindByEmail(self):
        try:
            db, teardown = TestDB(database_config)
            s = Store(db)
            u1 = TestUser()
            _, err = s.User().FindByEmail(u1.Email)
            self.assertEqual(err, ErrRecordNotFound)

            s.User().Create(u1)
            u2, err = s.User().FindByEmail(u1.Email)
            self.assertIsNone(err)
            self.assertIsNotNone(u2)
        finally:
            teardown("users")


if __name__ == '__main__':
    unittest.main()
