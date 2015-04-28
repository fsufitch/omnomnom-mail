from sqlalchemy import create_engine, Column,  ForeignKey, Table
from sqlalchemy.types import DateTime, Integer, String, Text
#from sqlalchemy.types import Unicode as UString
#from sqlalchemy.types import UnicodeText as UText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

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
        self._engine = create_engine(url, pool_recycle=True, encoding='utf-8')
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

email_to_address_association_table = Table('email_to_address', manager.base.metadata,
    Column('email_id', Integer, ForeignKey('emails.id')),
    Column('address_id', Integer, ForeignKey('addresses.id'))
)

class Email(manager.base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)

    # Many to one
    origin_id = Column(Integer, ForeignKey('addresses.id'))
    origin = relationship('EmailAddress', backref='emails_sent')
    
    # Many to many
    recipients = relationship('EmailAddress', secondary=email_to_address_association_table,
                              backref='emails_received')

    # One to many
    headers = relationship('EmailHeader', backref='email')
    
    subject = Column(String(1000))
    original = Column(Text)
    body_plain = Column(Text)
    body_html = Column(Text)
    recv_time = Column(DateTime, index=True)

class EmailAddress(manager.base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    address = Column(String(100), index=True, unique=True)
    name = Column(String(100), nullable=True)

class EmailHeader(manager.base):
    __tablename__ = 'headers'

    id = Column(Integer, primary_key=True)
    key = Column(String(100), index=True)
    value = Column(String(2000))
    email_id = Column(Integer, ForeignKey('emails.id'))
