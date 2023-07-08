import unittest

from app.store.errors import ErrRecordNotFound
from .test_store import (
    database_config,
    MainTest
)

from app.model import TestUser
from .testing import TestDB
from . import Store


class UserRepositoryTest(MainTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_Create(self):
        db, teardown = TestDB(database_config)
        s = Store(db)
        u = TestUser()
        err = s.User().Create(u)
        self.assertIsNone(err)
        self.assertTrue(hasattr(u, "ID"))
        teardown("users")

    def test_FindByEmail(self):
        db, teardown = TestDB(database_config)
        s = Store(db)
        u1 = TestUser()
        _, err = s.User().FindByEmail(u1.Email)
        self.assertEqual(err, ErrRecordNotFound)

        s.User().Create(u1)
        u2, err = s.User().FindByEmail(u1.Email)
        self.assertIsNone(err)
        self.assertIsNotNone(u2)

        teardown("users")


if __name__ == '__main__':
    unittest.main()
