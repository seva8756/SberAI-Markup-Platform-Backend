import http
import os
import shutil
import unittest

from flask import Flask
from flask_jwt_extended import create_access_token

from app.controllers.tests.testing import TestConfig
from app.model import TestUser
from app.model.testing import TestProject
from app.server import Server

from app.store.teststore import TestStore
from app.utils import utils


def get_task(s: Flask, user_id: int, project_id: int):
    with s.app_context():
        access_token = create_access_token(identity=user_id)
    client = s.test_client()
    client.set_cookie('access_token', access_token)
    response = client.get(f'/projects/task-selection/{project_id}')
    return response.json.get('index')


def answer_task(s: Flask, user_id: int, project_id: int, task_id: int, answer="answer"):
    with s.app_context():
        access_token = create_access_token(identity=user_id)
    client = s.test_client()
    client.set_cookie('access_token', access_token)
    response = client.post(f'/projects/task-answer',
                           json={"project_id": project_id, "task_id": task_id, "answer": answer})
    return response.json


class ProjectControllerTest(unittest.TestCase):
    def setUp(self):
        data_directory = utils.get_project_root() + '/data/projects'
        test_store_directory = utils.get_project_root() + '/app/file_store/testing'
        projects = ["test_project", "testchoice_project"]
        for p in projects:
            # Удаление папки test_project, если она существует
            test_project_directory = os.path.join(data_directory, p)
            # Копирование папки test_store
            shutil.copytree(test_store_directory + f"/{p}", test_project_directory)

    def tearDown(self) -> None:
        data_directory = utils.get_project_root() + '/data/projects'
        projects = ["test_project", "testchoice_project"]
        for p in projects:
            test_project_directory = os.path.join(data_directory, p)
            if os.path.exists(test_project_directory):
                shutil.rmtree(test_project_directory)

    def test_HandleProjectsGetAll(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask

        u = TestUser()
        store.User().Create(u)

        p = TestProject()
        store.Project().Create(p)
        store.Project().Join(p.ID, u.ID)
        with s.app_context():
            access_token = create_access_token(identity=u.ID)

        testCases = (
            {
                "name": "valid",
                "token": access_token,
                "expectedCode": http.HTTPStatus.OK
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                client = s.test_client()
                client.set_cookie('access_token', val["token"])
                response = client.get('/projects/all')
                self.assertEqual(response.status_code, val["expectedCode"])

    def test_HandleProjectsGetTask(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask

        def valid():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)

            store.Project().Join(p.ID, u.ID)
            return p, u

        def project_not_found():
            p = TestProject()
            p.ID = 111
            u = TestUser()
            store.User().Create(u)

            store.Project().Join(p.ID, u.ID)
            return p, u

        def no_access_to_project():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)

            return p, u

        def no_tasks_available():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)
            store.Project().Join(p.ID, u.ID)

            for iter in range(50):
                task_id = get_task(s, u.ID, p.ID)
                answer_task(s, u.ID, p.ID, task_id)

            return p, u

        testCases = (
            {
                "name": "valid",
                "units": valid,
                "expectedCode": http.HTTPStatus.OK
            },
            {
                "name": "project_not_found",
                "units": project_not_found,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
            {
                "name": "no_access_to_project",
                "units": no_access_to_project,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
            {
                "name": "no_tasks_available",
                "units": no_tasks_available,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                client = s.test_client()
                p, u = val["units"]()
                with s.app_context():
                    access_token = create_access_token(identity=u.ID)
                client.set_cookie('access_token', access_token)
                response = client.get(f'/projects/task-selection/{p.ID}')
                self.assertEqual(response.status_code, val["expectedCode"])

    def test_HandleProjectsAnswerTask(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask

        def valid():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)
            store.Project().Join(p.ID, u.ID)

            task_id = get_task(s, u.ID, p.ID)
            return u, p, task_id

        def project_not_found():
            p = TestProject()
            p.ID = 111
            u = TestUser()
            store.User().Create(u)
            store.Project().Join(p.ID, u.ID)

            task_id = -1
            return u, p, task_id

        def answer_option_does_not_exist():
            p = TestProject(directory="testchoice_project")
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)
            store.Project().Join(p.ID, u.ID)

            task_id = get_task(s, u.ID, p.ID)
            return u, p, task_id

        def task_not_reserved_for_user():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)
            store.Project().Join(p.ID, u.ID)

            task_id = 1
            return u, p, task_id

        def task_not_found():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)
            store.Project().Join(p.ID, u.ID)

            task_id = 99999
            return u, p, task_id

        testCases = (
            {
                "name": "valid",
                "payload": valid,
                "expectedCode": http.HTTPStatus.OK
            },
            {
                "name": "project_not_found",
                "payload": project_not_found,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
            {
                "name": "answer_option_does_not_exist",
                "payload": answer_option_does_not_exist,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
            {
                "name": "task_not_reserved_for_user",
                "payload": task_not_reserved_for_user,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
            {
                "name": "task_not_found",
                "payload": task_not_found,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                client = s.test_client()
                u, p, task_id = val["payload"]()
                with s.app_context():
                    access_token = create_access_token(identity=u.ID)
                client.set_cookie('access_token', access_token)
                response = client.post(f'/projects/task-answer',
                                       json={"project_id": p.ID, "task_id": task_id, "answer": "answer"})
                self.assertEqual(response.status_code, val["expectedCode"])

    def test_HandleProjectsJoin(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask

        def valid():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)

            project_code = utils.ProjectCode.encode_id(p.ID)

            return project_code, u

        def project_not_found():
            p = TestProject()
            p.ID = 111
            u = TestUser()
            store.User().Create(u)

            project_code = utils.ProjectCode.encode_id(p.ID)

            return project_code, u

        def wrong_password():
            p = TestProject()
            store.Project().Create(p)
            u = TestUser()
            store.User().Create(u)

            project_code = utils.ProjectCode.encode_id(p.ID)

            return project_code, u

        testCases = (
            {
                "name": "valid",
                "payload": valid,
                "expectedCode": http.HTTPStatus.OK
            },
            {
                "name": "project_not_found",
                "payload": project_not_found,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
            {
                "name": "wrong_password",
                "payload": wrong_password,
                "expectedCode": http.HTTPStatus.FORBIDDEN
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                client = s.test_client()
                code, u = val["payload"]()
                with s.app_context():
                    access_token = create_access_token(identity=u.ID)
                client.set_cookie('access_token', access_token)

                password = "test"
                if val["name"] == "wrong_password":
                    password = "testtest"

                response = client.post(f'/projects/join',
                                       json={"code": code, "password": password})
                self.assertEqual(response.status_code, val["expectedCode"])


if __name__ == '__main__':
    unittest.main()
