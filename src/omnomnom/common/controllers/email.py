from datetime import datetime
from omnomnom.common.db import Email, EmailHeader

class EmailController(object):
    def __init__(self, session):
        self.session = session

    def get_newest(self, number=5):
        query = self.session.query(Email).order_by(Email.recv_time.desc())
        return query[:5]

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
        payload = EmailController.get_payload_str(message)
        headers = self.build_headers(message)
            
        mail = Email(origin=from_addr,
                     recipients=to_addrs,
                     headers=headers,
                     subject=message['Subject'],
                     body=payload,
                     recv_time=datetime.utcnow()
        )
        
        self.session.add(mail)
        if commit:
            self.session.commit()
        return mail

    @staticmethod
    def get_payload_str(message):
        parts = []
        for part in message.walk():
            if part.is_multipart():
                continue # Only render leaves into text
            payload = part.get_payload(decode=True) # bytes
            payload = payload.decode()
            parts.append(payload)
        payload_str = ''.join(parts)
        return payload_str
