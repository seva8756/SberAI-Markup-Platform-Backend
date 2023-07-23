import http
import unittest

from app.controllers.tests.testing import TestConfig
from app.model import TestUser
from app.model.testing import TestToken
from app.server import Server

from app.store.teststore import TestStore


class UserControllerTest(unittest.TestCase):
    def test_HandleUsersCreate(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask.test_client()
        u = TestUser()
        store.User().Create(u)
        testCases = (
            {
                "name": "valid",
                "payload": {"email": u.Email, "password": u.Password},
                "expectedCode": http.HTTPStatus.CREATED
            },
            {
                "name": "invalid",
                "payload": "invalid",
                "expectedCode": http.HTTPStatus.BAD_REQUEST
            },
            {
                "name": "invalid params",
                "payload": {"email": "invalid", "password": "short"},
                "expectedCode": http.HTTPStatus.UNPROCESSABLE_ENTITY
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                response = s.post('/users/create',
                                  json=val["payload"])
                self.assertEqual(response.status_code, val["expectedCode"])

    def test_HandleUsersLogin(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask.test_client()
        u = TestUser()
        store.User().Create(u)
        testCases = (
            {
                "name": "valid",
                "payload": {"email": u.Email, "password": u.Password},
                "expectedCode": http.HTTPStatus.OK
            },
            {
                "name": "invalid",
                "payload": "invalid",
                "expectedCode": http.HTTPStatus.BAD_REQUEST
            },
            {
                "name": "invalid auth data",
                "payload": {"email": "invalid", "password": "short"},
                "expectedCode": http.HTTPStatus.UNAUTHORIZED
            },
            {
                "name": "invalid auth password",
                "payload": {"email": u.Email, "password": "short"},
                "expectedCode": http.HTTPStatus.UNAUTHORIZED
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                response = s.post('/users/login',
                                  json=val["payload"])
                self.assertEqual(response.status_code, val["expectedCode"])

    def test_HandleUsersRefresh(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask
        with s.app_context():
            t = TestToken(generate_valid=True)
            invalid_refresh = TestToken(user=1, generate_valid=True)

        store.Token().Create(t)
        testCases = (
            {
                "name": "valid",
                "token": t.refresh_token,
                "expectedCode": http.HTTPStatus.OK
            },
            {
                "name": "invalid",
                "token": "invalid",
                "expectedCode": http.HTTPStatus.UNPROCESSABLE_ENTITY
            },
            {
                "name": "invalid auth data",
                "token": invalid_refresh.refresh_token,
                "expectedCode": http.HTTPStatus.UNAUTHORIZED
            },
        )

        for val in testCases:
            with self.subTest(val["name"]):
                response = s.test_client().post('/users/refresh',
                                                headers={'Authorization': 'Bearer ' + val["token"]})
                self.assertEqual(response.status_code, val["expectedCode"])


if __name__ == '__main__':
    unittest.main()
