import os
import unittest
from model.db_model import Session, User, File, FileType
from tests.db_model import setup_db_model


def setUpModule():
    setup_db_model()


class TestDbModel(unittest.TestCase):
    def test_base(self):
        session = Session()
        user = User(username='lee', password='123456')
        self.assertIsNone(user.id)
        session.add(user)
        session.commit()
        self.assertIsNotNone(user.id)
