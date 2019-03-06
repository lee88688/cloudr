from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_URL


engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(40), nullable=False)

    def __repr__(self):
        return '<User({}) {}>'.format(self.id, self.username)


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id'), nullable=False)
    filetype = Column(Integer, ForeignKey('file_type.id'), nullable=False)
    filename = Column(String(40), nullable=False)
    filesize = Column(Integer)
    uploaddate = Column(DateTime, nullable=False)
    path = Column(Text, nullable=False)
    md5 = Column(String(40), nullable=False)

    def __repr__(self):
        return '<File({}) {} {}>'.format(self.id, self.filename, self.path)


class FileType(Base):
    __tablename__ = 'file_type'

    id = Column(Integer, primary_key=True)
    filetype = Column(String(10))

    @classmethod
    def insert_all_types(cls):
        from utils.filetype import file_types
        session = Session()
        type_list = []
        for t in file_types:
            type_list.append(cls(filetype=t))
        session.add_all(type_list)
        session.commit()

    def __repr__(self):
        return '<FileType({}) {}>'.format(self.id, self.filetype)


class OfflineDownload(Base):
    __tablename__ = 'offline_download'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('user.id'), nullable=False)
    filename = Column(String(40))
    path = Column(Text)
    url = Column(Text, nullable=False)
    gid = Column(String(16))
    completed = Column(Integer, nullable=False)  # from 0 to 100 percent
    done = Column(Boolean, nullable=False)
    time = Column(DateTime, nullable=False)
    error = Column(Integer)
    message = Column(Text)

    def __repr__(self):
        return '<offline_download({}) {} {}%>'.format(self.id, self.filename, self.completed)
