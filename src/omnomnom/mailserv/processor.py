import re

from omnomnom.common.db import manager, Email, EmailAddress, EmailHeader
from omnomnom.common.controllers.email import EmailController
from omnomnom.common.controllers.address import AddressController
from omnomnom.mailserv import logger

class EmailProcessor(object):
    def __init__(self):
        self.session = manager.create_session()
        self.emailctl = EmailController(self.session)
        self.addressctl = AddressController(self.session)
        
    def record_email(self, recipients, message):
        if message.get('From', None):
            addr, name = AddressController.parse_addresses(message['From'])[0]
        else:
            logger.info("Dropping email; could not extract origin address")
            return

        from_addr = self.addressctl.update_address(addr, name, commit=False)
        
        to_addrs = []
        for addr_str in recipients:
            if not addr_str.endswith('@omnomnom.email'):
                continue
            to_addr = self.addressctl.update_address(addr_str, commit=False)
            to_addrs.append(to_addr)
        if not to_addrs and recipients and recipients[0].endswith('@omnomnom.email'):
            to_addr = self.addressctl.update_address(recipients[0], commit=False)
            to_addrs.append(to_addr)

        if not to_addrs:
            logger.info("Dropping email; no valid recipients (origin: %s)" % from_addr.address)
            self.session.rollback()
            return

        logger.debug("Recording email from <%s> to: " % (from_addr.address, to_addrs))
        self.emailctl.record_email(from_addr, to_addrs, message, commit=False)
        self.session.commit()
        logger.debug("Committed!")

    def __del__(self):
        self.session.close()

