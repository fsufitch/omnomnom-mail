from tornado.web import RequestHandler

from omnomnom.common.db import manager as db_manager
from omnomnom.common.controllers.address import AddressController
from omnomnom.common.controllers.email import EmailController
from omnomnom.webui.util import apply_template, write_return, HTTPErrorResponse

class SenderViewHandler(RequestHandler):
    @write_return
    @apply_template("sender_browse.html")
    def get(self, email):
        email = email.strip().lower()
        page_data = {
            'found': True,
            'address': email,
        }
        with HTTPErrorResponse(self, 400, "invalid pagination"):
            start_index = int(self.get_argument("start", 0))
            page_length = int(self.get_argument("count", 20))
            if start_index < 0 or page_length < 1:
                raise ValueError("Invalid index/length: %s, %s" % (start_index, page_length))

        session = db_manager.create_session()
        address_ctl = AddressController(session)
        email_ctl = EmailController(session)

        address = address_ctl.search_by_address(email)
        mails = email_ctl.get_by_sender(address)

        page_data['name'] = address.name

        mail_data = []
        for mail in mails:
            sender = (mail.origin.address, mail.origin.name)
            mail_data.append( (sender, mail.subject, mail.recv_time) )
        page_data['mails'] = mail_data
            
        session.close()
        
        return page_data
