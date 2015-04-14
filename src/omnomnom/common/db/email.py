from sqlalchemy import Column, Integer, String, Text

from omnomnom.common.db.base import manager

class Email(manager.base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True)
    from_addr = Column(String)
    to_addrs = Column(String)
    subject = Column(String)
    body = Column(Text)
