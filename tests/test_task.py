import os
import unittest
from model.db_model import Session, User, FileType
from tests.db_model import setup_db_model


def setUpModule():
    setup_db_model()


class TestAddUri(unittest.TestCase):
    def setUp(self):
        session = Session()
        user = User(username='task', password='123456')
        session.add(user)
        session.commit()

    def test_addUri(self):
        session = Session()
        user = session.query(User).filter(User.username == 'lee').first()
        self.assertIsNotNone(user.id)


if __name__ == "__main__":
    unittest.main()
