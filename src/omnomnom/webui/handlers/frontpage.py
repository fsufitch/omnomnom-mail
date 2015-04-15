from tornado.web import RequestHandler

from omnomnom.common.db import manager as db_manager
from omnomnom.common.db import Email

class FrontPageHandler(RequestHandler):
    def get(self):
        self.set_header("Content-type", "text/plain")
        self.write("hi\n")

        session = db_manager.create_session()
        for email in session.query(Email).all():
            self.write("FROM: " + email.from_addr)
            self.write("TO: " + email.to_addrs)
            self.write("SUBJECT: " + email.subject)
            self.write("BODY:\n" + email.body)
            self.write("\n\n============ END BODY ==========\n\n")
