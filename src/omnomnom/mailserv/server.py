import argparse, asyncore, email
from smtpd import SMTPServer
from yaul.init import InitService

from omnomnom.common.config import Configuration
from omnomnom.common.db import manager as db_manager
from omnomnom.common.logging import setup_logging
from omnomnom.mailserv import logger
from omnomnom.mailserv.processor import EmailProcessor

PID_PATH = "/var/run/omnomnom_smtpd.pid"
CONFIG_PATH = "/etc/omnomnom/smtpd.json"

class OmnomnomSMTPServer(SMTPServer):
    def __init__(self, hostname, port, conf):
        super(OmnomnomSMTPServer, self).__init__( (hostname, port), None)
        self.conf = conf
        self.processor = EmailProcessor()
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        try:
            msg = email.message_from_string(data)
            self.processor.record_email(rcpttos, msg)
        except Exception as e:
            logger.exception(e)
        
    @staticmethod
    def run_server(conf):
        hostname = conf.get('hostname')
        port = conf.get('port', default=25)

        setup_logging(conf.get('logging', 'file'),
                      conf.get('logging', 'debug', default=False))

        logger.debug("creating db")
        db_manager.create_db(conf.get('db'))
        
        server = OmnomnomSMTPServer(hostname, port, conf)
        logger.info("listening on %s:%s" % (hostname, port))
        asyncore.loop()
        
def main():
    parser = argparse.ArgumentParser(description="Omnomnom SMTP server")
    parser.add_argument("config", nargs="?", default=CONFIG_PATH,
                        help="JSON configuration file")
    args = parser.parse_args()
    config = Configuration(args.config)
    OmnomnomSMTPServer.run_server(config)

def service_main():
    pid_path = PID_PATH
    config = Configuration(CONFIG_PATH)
    pid_path = config.get('pid', default=pid_path)

    service = InitService(pid_path, OmnomnomSMTPServer.run_server, args=[config], fork=True)
    service.run_cmdline()
