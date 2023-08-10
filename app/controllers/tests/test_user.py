import http
import unittest

from flask_jwt_extended import create_access_token

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
                "payload": {"email": u.email, "password": u.password, "first_name": u.first_name,
                            "last_name": u.last_name},
                "expectedCode": http.HTTPStatus.CREATED
            },
            {
                "name": "invalid",
                "payload": "invalid",
                "expectedCode": http.HTTPStatus.BAD_REQUEST
            },
            {
                "name": "invalid params",
                "payload": {"email": "invalid", "password": "short", "first_name": "", "last_name": ""},
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
                "payload": {"email": u.email, "password": u.password},
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
                "payload": {"email": u.email, "password": "short"},
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
                client = s.test_client()
                client.set_cookie('refresh_token', val["token"])
                response = client.post('/users/refresh')
                self.assertEqual(response.status_code, val["expectedCode"])

    def test_HandleUsersGetInfoPersonal(self):
        store = TestStore()
        s = Server(store, TestConfig()).flask

        u = TestUser()
        store.User().Create(u)
        with s.app_context():
            access_token = create_access_token(identity=u.ID)
            access_token_not_found = create_access_token(identity=123)

        testCases = (
            {
                "name": "valid",
                "token": access_token,
                "expectedCode": http.HTTPStatus.OK
            },
            {
                "name": "not found",
                "token": access_token_not_found,
                "expectedCode": http.HTTPStatus.NOT_FOUND
            },
            {
                "name": "invalid",
                "token": "invalid",
                "expectedCode": http.HTTPStatus.UNPROCESSABLE_ENTITY
            }
        )

        for val in testCases:
            with self.subTest(val["name"]):
                client = s.test_client()
                client.set_cookie('access_token', val["token"])
                response = client.get('/users/info/personal')
                self.assertEqual(response.status_code, val["expectedCode"])


if __name__ == '__main__':
    unittest.main()
