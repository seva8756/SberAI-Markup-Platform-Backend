import unittest

from app.model.testing import TestToken
from app.store.errors import ErrRecordNotFound

from app.store.sqlstore.testing import TestStore


class UserRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_Create(self):
        try:
            s, teardown = TestStore()
            t = TestToken()

            err = s.Token().Create(t)
            self.assertIsNone(err)
            self.assertTrue(hasattr(t, "ID"))
        finally:
            teardown("sessions")

    def test_FindByRefresh(self):
        try:
            s, teardown = TestStore()
            t1 = TestToken()
            _, err = s.Token().FindByRefresh(t1.refresh_token)
            self.assertEqual(err, ErrRecordNotFound)

            s.Token().Create(t1)
            t2, err = s.Token().FindByRefresh(t1.refresh_token)
            self.assertIsNone(err)
            self.assertIsNotNone(t2)
        finally:
            teardown("sessions")

    def test_Reset(self):
        try:
            s, teardown = TestStore()
            t1 = TestToken()
            err = s.Token().Reset(t1.refresh_token)
            self.assertEqual(err, ErrRecordNotFound)

            s.Token().Create(t1)
            err = s.Token().Reset(t1.refresh_token)
            self.assertIsNone(err)
        finally:
            teardown("sessions")

    def test_Update(self):
        try:
            s, teardown = TestStore()
            t1 = TestToken()
            err = s.Token().Update(t1)
            self.assertIsNotNone(err)

            s.Token().Create(t1)
            err = s.Token().Update(t1)
            self.assertIsNone(err)
        finally:
            teardown("sessions")


if __name__ == '__main__':
    unittest.main()
