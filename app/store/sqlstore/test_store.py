import unittest

database_config: dict = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "markup-platform-test"
}


class MainTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        # global database_config
        # database_config = {
        #     "host": "localhost",
        #     "user": "root",
        #     "password": "root",
        #     "database": "markup-platform-test"
        # }


if __name__ == '__main__':
    unittest.main()
