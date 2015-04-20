from tornado.web import RequestHandler

from omnomnom.common.db import manager as db_manager
from omnomnom.common.controllers.email import EmailController
from omnomnom.common.wordgen.generator import NameGenerator
from omnomnom.webui.util import apply_template, write_return

class FrontPageHandler(RequestHandler):
    @write_return
    @apply_template("frontpage.html")
    def get(self):
        self.set_header("Content-type", "text/html")
        session = db_manager.create_session()

        emailctl = EmailController(session)
        newest_emails = emailctl.get_newest(5)

        email_data = []
        for email in newest_emails:
            email_data.append({
                'subject': email.subject,
                'recv_time': email.recv_time,
                'origin_address': email.origin.address,
                'recipient_address': email.recipients[0].address,
                'num_hidden_recipients': len(email.recipients)-1,
                })

        #session.close()
        
        ng = NameGenerator.instance()
        random_email = "{adj}_{noun}@omnomnom.email".format(
            adj=ng.random_adjective(),
            noun=ng.random_noun()
        )

        return {'newest_emails': email_data,
                'random_email': random_email}
