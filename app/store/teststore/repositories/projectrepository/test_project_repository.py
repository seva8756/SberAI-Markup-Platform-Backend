import unittest

from app.model.testing import TestProject
from app.store.teststore import TestStore
from app.model import TestUser
from app.store.errors import ErrRecordNotFound


class ProjectRepositoryTest(unittest.TestCase):
    def test_Create(self):
        s = TestStore()
        u = TestProject()
        self.assertIsNone(s.Project().Create(u))

    def test_Update(self):
        s = TestStore()
        p = TestProject()

        err = s.Project().Update(p)
        self.assertIsInstance(err, AttributeError)

        s.Project().Create(p)
        p.directory = "test2_project"
        s.Project().Update(p)
        self.assertEqual(s.Project().projects[p.ID].directory, "test2_project")

    def test_FindAllByUserId(self):
        s = TestStore()
        p = TestProject()
        u = TestUser()
        s.User().Create(u)

        s.Project().Create(p)
        err = s.Project().Join(p.ID, u.ID)

        self.assertIsNone(err)
        self.assertEqual(len(s.Project().projects_participants[p.ID]), 1)
        self.assertEqual(s.Project().projects_participants[p.ID][0], u.ID)

    def test_Find(self):
        s = TestStore()

        found_project, err = s.Project().Find(1)
        self.assertIsNone(found_project)
        self.assertEqual(err, ErrRecordNotFound)

        p = TestProject()
        s.Project().Create(p)
        found_project, err = s.Project().Find(p.ID)

        self.assertIsNone(err)
        self.assertIsNotNone(found_project)
        self.assertEqual(found_project.ID, p.ID)

    def test_FindCompletedTasks(self):
        s = TestStore()
        p = TestProject()
        u = TestUser()
        s.User().Create(u)
        s.Project().Create(p)

        tasks, err = s.Project().FindCompletedTasks(u.ID, p.ID)
        self.assertEqual(tasks, [])

        s.Project().SetAnswer(p.ID, 1, u.ID, "answer2", 1)
        tasks, err = s.Project().FindCompletedTasks(u.ID, p.ID)

        self.assertIsNone(err)
        self.assertEqual(len(tasks), 1)

    def test_FindCompletedTasks(self):
        s = TestStore()
        p = TestProject()
        u = TestUser()
        s.User().Create(u)
        s.Project().Create(p)

        tasks, err = s.Project().FindUserCompletedTasks(u.ID)
        self.assertEqual(tasks, [])

        s.Project().SetAnswer(p.ID, 1, u.ID, "answer2", 1)
        tasks, err = s.Project().FindUserCompletedTasks(u.ID)

        self.assertIsNone(err)
        self.assertEqual(len(tasks), 1)

    def test_isParticipant(self):
        s = TestStore()
        p = TestProject()
        u = TestUser()
        s.User().Create(u)
        s.Project().Create(p)

        is_participant, err = s.Project().isParticipant(p.ID, u.ID)
        self.assertIsNone(err)
        self.assertFalse(is_participant)

        s.Project().Join(p.ID, u.ID)
        is_participant, err = s.Project().isParticipant(p.ID, u.ID)
        self.assertIsNone(err)
        self.assertTrue(is_participant)

    def test_Join(self):
        s = TestStore()
        u = TestUser()
        s.User().Create(u)

        p = TestProject()
        s.Project().Create(p)
        err = s.Project().Join(p.ID, u.ID)

        self.assertIsNone(err)
        self.assertEqual(len(s.Project().projects_participants[p.ID]), 1)
        self.assertEqual(s.Project().projects_participants[p.ID][0], u.ID)

    def test_SetAnswer(self):
        s = TestStore()
        u = TestUser()
        s.User().Create(u)

        p = TestProject()
        s.Project().Create(p)
        err = s.Project().SetAnswer(p.ID, 1, u.ID, "answer", 1)
        self.assertEqual(s.Project().completed_tasks[0]["answer"], "answer")
        self.assertIsNone(err)

        err = s.Project().SetAnswer(p.ID, 1, u.ID, "answer2", 1)
        self.assertEqual(s.Project().completed_tasks[0]["answer"], "answer2")
        self.assertIsNone(err)


if __name__ == '__main__':
    unittest.main()
