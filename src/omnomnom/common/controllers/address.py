import re
from omnomnom.common.db import EmailAddress

class AddressController(object):
    NAME_ADDR_EXP = re.compile('(?:(.*)<(.*)>)|(.*)')

    def __init__(self, session):
        self.session = session

    def update_address(self, address, name='', commit=True):
        address = address.lower()
        name = name.strip()
        query = self.session.query(EmailAddress).filter(EmailAddress.address==address)
        email_address = None
        if query.count():
            email_address = query.one()
            if not email_address.name and name:
                email_address.name = name
        else:
            email_address = EmailAddress(address=address,
                                         name=name or None)
            self.session.add(email_address)
        if commit:
            self.session.commit()
        return email_address

    @staticmethod
    def parse_addresses(addr_str):
        separated = addr_str.split(',')
        addr_name_tuples = []
        for addr in separated:
            addr = addr.strip()
            name = ''
            email = None
            match = AddressController.NAME_ADDR_EXP.search(addr)
            if match.groups()[2]:
               # Plain address 
               email = match.groups()[2]
            else:
                name = match.groups()[0]
                email = match.groups()[1]
            email = email.lower()
            addr_name_tuples.append( (email, name) )
        return addr_name_tuples
