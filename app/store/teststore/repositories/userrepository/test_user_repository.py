import unittest
from app.store.teststore import TestStore
from app.model import TestUser
from app.store.teststore.repositories.userrepository.user_repository import *


class UserRepositoryTest(unittest.TestCase):
    def test_Create(self):
        s = TestStore()
        u = TestUser()
        self.assertIsNone(s.User().Create(u))

    def test_FindByEmail(self):
        s = TestStore()
        u1 = TestUser()
        _, err = s.User().FindByEmail(u1.email)
        self.assertEqual(err, ErrRecordNotFound)

        s.User().Create(u1)
        u2, err = s.User().FindByEmail(u1.email)
        self.assertIsNone(err)
        self.assertIsNotNone(u2)

    def test_Find(self):
        s = TestStore()
        u1 = TestUser()
        _, err = s.User().Find(1)
        self.assertEqual(err, ErrRecordNotFound)

        s.User().Create(u1)
        u2, err = s.User().Find(u1.ID)
        self.assertIsNone(err)
        self.assertIsNotNone(u2)
