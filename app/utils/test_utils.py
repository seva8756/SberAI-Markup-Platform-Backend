import unittest

from app.utils import utils


class UtilsTest(unittest.TestCase):
    def test_Project_Encode_id(self):
        code = utils.ProjectCode.encode_id(1)
        self.assertEqual(code, "PRJA")
        code = utils.ProjectCode.encode_id(111)
        self.assertEqual(code, "PRJDG")

    def test_Project_Decode_id(self):
        code = utils.ProjectCode.decode_id("PRJA")
        self.assertEqual(code, 1)
        code = utils.ProjectCode.decode_id("PRJDG")
        self.assertEqual(code, 111)


if __name__ == '__main__':
    unittest.main()
