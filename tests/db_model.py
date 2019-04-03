import os
from model.db_model import Base, engine, FileType


os.environ['DB_URL'] = 'sqlite:///:memory:'


def setup_db_model():
    # in one test, different case use same db
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    FileType.insert_all_types()
