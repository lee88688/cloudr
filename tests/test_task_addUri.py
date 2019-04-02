import os
import unittest


class TestAddUri(unittest.TestCase):
    def setUp(self):
        os.environ['DB_URL'] = 'sqlite:///:memory:'

    def test_addUri(self):
        pass


if __name__ == "__main__":
    unittest.main()
