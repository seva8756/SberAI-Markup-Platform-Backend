import unittest

from app.model.testing import TestToken
from app.store.errors import ErrRecordNotFound

from app.store.teststore import TestStore


class TokenRepositoryTest(unittest.TestCase):
    def test_Create(self):
        s = TestStore()
        t = TestToken()
        self.assertIsNone(s.Token().Create(t))
        self.assertEqual(len(s.Token().sessions), 1)
        self.assertEqual(s.Token().sessions[t.ID], t)

    def test_Update(self):
        s = TestStore()

        t = TestToken()
        s.Token().Create(t)
        t.refresh_token = "new_test_refresh_token"
        self.assertIsNone(s.Token().Update(t))
        self.assertEqual(s.Token().sessions[t.ID].refresh_token, "new_test_refresh_token")

    def test_FindByRefresh(self):
        s = TestStore()

        t = TestToken(refresh_token="test_refresh_token")
        s.Token().Create(t)

        found_token, err = s.Token().FindByRefresh("test_refresh_token")
        self.assertEqual(found_token, t)
        self.assertIsNone(err)

        found_token, err = s.Token().FindByRefresh("non_existent_refresh_token")
        self.assertIsNone(found_token)
        self.assertEqual(err, ErrRecordNotFound)

    def test_Reset(self):
        s = TestStore()

        t = TestToken(refresh_token="test_refresh_token")
        s.Token().Create(t)

        err = s.Token().Reset("test_refresh_token")
        self.assertIsNone(err)
        self.assertEqual(len(s.Token().sessions), 0)

        err = s.Token().Reset("non_existent_refresh_token")
        self.assertEqual(err, ErrRecordNotFound)


if __name__ == '__main__':
    unittest.main()
