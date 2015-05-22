from tornado.web import RequestHandler, HTTPError

from omnomnom.common.db import manager as db_manager
from omnomnom.common.controllers.email import EmailController
from omnomnom.webui.util import write_return, apply_template

class EmailViewHandler(RequestHandler):
    @write_return
    @apply_template("email.html")
    def get(self, email_id):
        session = db_manager.create_session()
        controller = EmailController(session)

        email = controller.get_by_id(email_id)
        if not email:
            raise HTTPError(404)

        pagedata = {
            'email': {
                'id': email.id,
                'subject': email.subject,
                'recv_time': email.recv_time,
                'original': email.original[:1000],
                'original_truncated': len(email.original)>1000,
                'body_plain': email.body_plain[:1000],
                'body_plain_truncated': len(email.body_plain)>1000,
            },
            'sender': {
                'address': email.origin.address,
                'name': email.origin.name,
                'browse_url': self.reverse_url('sender_browse', email.origin.address)
            },
            'headers': [],
            'recipients': [],
        }
        for header in email.headers:
            hdr = (header.key, header.value)
            pagedata['headers'].append(hdr)
        for recipient in email.recipients:
            rec = {
                'address': recipient.address,
                'name': recipient.name,
            }
            pagedata['recipients'].append(rec)
        session.close()
        
        return pagedata
