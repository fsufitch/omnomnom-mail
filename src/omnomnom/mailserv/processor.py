import re

from omnomnom.common.db import manager, Email, EmailAddress, EmailHeader
from omnomnom.common.controllers.email import EmailController
from omnomnom.common.controllers.address import AddressController

class EmailProcessor(object):
    def __init__(self):
        self.session = manager.create_session()
        self.emailctl = EmailController(self.session)
        self.addressctl = AddressController(self.session)
        
    def record_email(self, recipients, message):
        addr, name = AddressController.parse_addresses(message['From'])[0]
        from_addr = self.addressctl.update_address(addr, name, commit=False)
        
        to_addrs = []
        for addr_str in recipients:
            to_addr = self.addressctl.update_address(addr_str, commit=False)
            to_addrs.append(to_addr)

        self.emailctl.record_email(from_addr, to_addrs, message, commit=False)
        self.session.commit()

