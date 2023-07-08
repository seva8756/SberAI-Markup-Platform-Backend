import unittest
from . import TestStore
from app.model import TestUser
from .userrepository import *


class UserRepositoryTest(unittest.TestCase):
    def test_Create(self):
        s = TestStore()
        u = TestUser()
        self.assertIsNone(s.User().Create(u))

    def test_FindByEmail(self):
        s = TestStore()
        u1 = TestUser()
        _, err = s.User().FindByEmail(u1.Email)
        self.assertEqual(err, ErrRecordNotFound)

        s.User().Create(u1)
        u2, err = s.User().FindByEmail(u1.Email)
        self.assertIsNone(err)
        self.assertIsNotNone(u2)
