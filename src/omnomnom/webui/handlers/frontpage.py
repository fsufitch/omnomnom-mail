from tornado.web import RequestHandler

from omnomnom.common.db import manager as db_manager
from omnomnom.common.db import Email

class FrontPageHandler(RequestHandler):
    def get(self):
        self.set_header("Content-type", "text/plain")
        self.write("hi\n")

        session = db_manager.create_session()
        for email in session.query(Email).all():
            self.write("\nFROM: " + email.from_addr)
            self.write("\nTO: " + email.to_addrs)
            self.write("\nSUBJECT: " + email.subject)
            self.write("\nBODY:\n" + email.body)
            self.write("\n\n============ END BODY ==========\n\n")
