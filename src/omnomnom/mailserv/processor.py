import re

from omnomnom.common.db import manager, Email, EmailAddress, EmailHeader

class EmailProcessor(object):
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
        
    NAME_ADDR_EXP = re.compile('(?:(.*)<(.*)>)|(.*)')
    @staticmethod
    def parse_addresses(addr_str):
        separated = addr_str.split(',')
        addr_name_tuples = []
        for addr in separated:
            addr = addr.strip()
            name = None
            email = None
            match = EmailProcessor.NAME_ADDR_EXP.search(addr)
            if match.groups()[2]:
               # Plain address 
               email = match.groups()[2]
            else:
                name = match.groups()[0]
                email = match.groups()[1]
            email = email.lower()
            addr_name_tuples.append( (email, name) )
        return addr_name_tuples

    @staticmethod
    def update_address(session, address, name=''):
        address = address.lower()
        name = name.strip()
        query = session.query(EmailAddress).filter(EmailAddress.address==address)
        email_address = None
        if query.count():
            email_address = query.one()
            if not email_address.name and name:
                email_address.name = name
        else:
            email_address = EmailAddress(address=address,
                                         name=name or None)
            session.add(email_address)
        return email_address
    
    @staticmethod
    def record_email(recipients, message):
        payload = EmailProcessor.get_payload_str(message)
        headers = message.items()

        session = manager.create_session()

        addr, name = EmailProcessor.parse_addresses(message['From'])[0]
        from_addr = EmailProcessor.update_address(session, addr, name)
        
        to_addrs = []
        for addr_str in recipients:
            to_addr = EmailProcessor.update_address(session, addr_str)
            to_addrs.append(to_addr)

        headers = []
        for k,v in headers:
            k = k.strip()
            v = v.strip()
            header = EmailHeader(key=k,
                                 value=v)
            headers.append(header)
            
        mail = Email(origin=from_addr,
                     recipients=to_addrs,
                     headers=headers,
                     subject=message['Subject'],
                     body=payload)
        
        session.add(mail)
        session.commit()

