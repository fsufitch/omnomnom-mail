from tornado.web import RequestHandler

class FrontPageHandler(RequestHandler):
    def get(self):
        self.write("hi")
