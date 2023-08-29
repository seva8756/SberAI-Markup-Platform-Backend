import unittest

from app.model.testing import TestProject, TestUser
from app.store.errors import ErrRecordNotFound

from app.store.sqlstore.testing import TestStore


class ProjectRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_Create(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            err = s.Project().Create(p)
            self.assertIsNone(err)
            self.assertTrue(hasattr(p, "ID"))
        finally:
            teardown("projects")

    def test_Update(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            err = s.Project().Update(p)
            self.assertIsNotNone(err)

            s.Project().Create(p)
            err = s.Project().Update(p)
            self.assertIsNone(err)
        finally:
            teardown("projects")

    def test_FindAllByUserId(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            s.Project().Create(p)
            u = TestUser()
            s.User().Create(u)

            data, err = s.Project().FindAllByUserId(u.ID)
            self.assertTrue(len(data) == 0)

            s.Project().Join(p.ID, u.ID)
            data, err = s.Project().FindAllByUserId(u.ID)
            self.assertTrue(len(data) == 1)
        finally:
            teardown("users", "projects", "projects_participants")

    def test_Find(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            s.Project().Create(p)

            data, err = s.Project().Find(p.ID)
            self.assertIsNotNone(data)

            data, err = s.Project().Find(111)
            self.assertEqual(err, ErrRecordNotFound)
        finally:
            teardown("projects")

    def test_isParticipant(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            s.Project().Create(p)
            u = TestUser()
            s.User().Create(u)

            is_participant, err = s.Project().isParticipant(p.ID, u.ID)
            self.assertFalse(is_participant)

            s.Project().Join(p.ID, u.ID)
            is_participant, err = s.Project().isParticipant(p.ID, u.ID)
            self.assertTrue(is_participant)
            self.assertIsNone(err)
        finally:
            teardown("users", "projects", "projects_participants")

    def test_Join(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            s.Project().Create(p)
            u = TestUser()
            s.User().Create(u)

            err = s.Project().Join(p.ID, u.ID)
            self.assertIsNone(err)

        finally:
            teardown("users", "projects", "projects_participants")

    def test_SetAnswer(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            s.Project().Create(p)
            u = TestUser()
            s.User().Create(u)

            err = s.Project().SetAnswer(p.ID, 1, u.ID, "answer", 1)
            self.assertIsNone(err)

        finally:
            teardown("users", "projects", "completed_tasks")

    def test_FindCompletedTasks(self):
        try:
            s, teardown = TestStore()
            p = TestProject()
            s.Project().Create(p)
            u = TestUser()
            s.User().Create(u)

            tasks, err = s.Project().FindCompletedTasks(u.ID, p.ID)
            self.assertEqual(tasks, [])
            self.assertIsNone(err)

        finally:
            teardown("users", "projects", "completed_tasks")


if __name__ == '__main__':
    unittest.main()
