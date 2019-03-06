import os
import unittest


class TestAddUri(unittest.TestCase):
    def setUp(self):
        os.environ['DB_URL'] = 'sqlite:///:memory:'


if __name__ == "__main__":
    unittest.main()
