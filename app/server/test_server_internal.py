import http
import os
import unittest
import requests

from .server import Server

from app.store.teststore import TestStore

from app.config import Config


class TestServer(unittest.TestCase):
    def test_HandleUsersCreate(self):
        s = Server(TestStore()).flask.test_client()
        response = s.post('/users')

        self.assertEqual(response.status_code, http.HTTPStatus.OK)


if __name__ == '__main__':
    unittest.main()
