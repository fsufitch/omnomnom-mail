from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DBManager(object):
    def __init__(self):
        self._engine = None
        self._base = None
        self._sessionmaker = None

    @property
    def engine(self):
        return self.get_engine()
        
    def get_engine(self, url=None):
        if self._engine:
            return self._engine
        if not url:
            raise TypeError("Must specify DB URL for first invocation")
        self._engine = create_engine(url, echo=True)
        return self._engine

    @property
    def base(self):
        if not self._base:
            self._base = declarative_base()
        return self._base

    _instance = None
    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def create_db(self, engine_url):
        engine = self.get_engine(engine_url)
        self.base.metadata.create_all(engine)

    def create_session(self):
        if not self._sessionmaker:
            self._sessionmaker = sessionmaker(bind=self.engine)
        return self._sessionmaker()
    
manager = DBManager.instance()

#########

class Email(manager.base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    from_addr = Column(String(1000))
    to_addrs = Column(String(8000))
    subject = Column(String(1000))
    body = Column(Text)

