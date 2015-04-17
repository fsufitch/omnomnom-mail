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

        ng = NameGenerator.instance()
        random_email = "{adj}_{noun}@omnomnom.email".format(
            adj=ng.random_adjective(),
            noun=ng.random_noun()
        )
        
        return {'newest_emails': newest_emails,
                'random_email': random_email}
