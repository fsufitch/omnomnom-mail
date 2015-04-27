import re

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from omnomnom.common.db import Email, EmailHeader
from omnomnom.common.util import EmailUtil
from omnomnom.common import logger

class EmailController(object):
    def __init__(self, session):
        self.session = session

    def count_all(self):
        return self.session.query(Email).count()
        
    def get_newest(self, number=5):
        query = self.session.query(Email).order_by(Email.recv_time.desc())
        return query[:5]

    def get_by_id(self, email_id):
        query = self.session.query(Email).filter(Email.id==email_id)
        try:
            return query.one()
        except NoResultFound:
            return None
    
    def build_headers(self, message):
        headers = []
        for k,v in message.items():
            k = k.strip()
            v = v.strip()
            header = EmailHeader(key=k,
                                 value=v)
            headers.append(header)
        return headers
    
    def record_email(self, from_addr, to_addrs, message, commit=True):
        headers = self.build_headers(message)

        original = EmailUtil.render_to_original(message)
        body_plain = EmailUtil.render_content(message, allow_html=False)
        logger.debug('Got plain body:')
        logger.debug(body_plain)
        body_html = EmailUtil.render_content(message, allow_html=True)
        logger.debug('Got HTML body:')
        logger.debug(body_html)
            
        mail = Email(origin=from_addr,
                     recipients=to_addrs,
                     headers=headers,
                     subject=message['Subject'],
                     original=original,
                     body_plain=body_plain,
                     body_html=body_html,
                     recv_time=datetime.utcnow()
        )
        
        self.session.add(mail)
        if commit:
            self.session.commit()
        return mail
