import argparse, asyncore

from pkg_resources import resource_filename
from tornado.ioloop import IOLoop
from tornado.web import Application, StaticFileHandler, URLSpec
from yaul.init import InitService

from omnomnom.common.config import Configuration
from omnomnom.common.db import manager as db_manager
from omnomnom.common.logging import setup_logging, log_http
from omnomnom.webui import logger
from omnomnom.webui.handlers.frontpage import FrontPageHandler

PID_PATH = "/var/run/omnomnom_webui.pid"
CONFIG_PATH = "/etc/omnomnom/webui.json"

PATHS = [
    URLSpec("/s/(.*)", StaticFileHandler, {'path': resource_filename(__name__, 'static')}),
    URLSpec("/", FrontPageHandler, name='frontpage'),
    ]

class OmnomnomWebUIServer(object):
    @staticmethod
    def run_server(conf):
        hostname = conf.get('hostname')
        port = conf.get('port', default=80)

        setup_logging(conf.get('logging', 'file'),
                      conf.get('logging', 'debug', default=False))

        logger.debug('creating db...')
        db_manager.create_db(conf.get('db'))

        application = Application(PATHS)
        application.configuration = conf
        application.listen(port, address=hostname)
        application.log_request = log_http
        logger.debug('listening on %s:%s' % (hostname, port))
        IOLoop.instance().start()

def main():
    parser = argparse.ArgumentParser(description="Omnomnom web UI HTTP server")
    parser.add_argument("config", nargs="?", default=CONFIG_PATH,
                        help="JSON configuration file")
    args = parser.parse_args()
    config = Configuration(args.config)
    OmnomnomWebUIServer.run_server(config)

def service_main():
    pid_path = PID_PATH
    config = Configuration(CONFIG_PATH)
    pid_path = config.get('pid', default=pid_path)

    service = InitService(pid_path, OmnomnomWebUIServer.run_server, args=[config], fork=True)
    service.run_cmdline()
