import argparse, asyncore, email
from smtpd import SMTPServer

from omnomnom.common.config import Configuration
from omnomnom.common.db import manager as db_manager
from omnomnom.mailserv.processor import EmailProcessor

class OmnomnomSMTPServer(SMTPServer):
    def __init__(self, hostname, port, conf):
        super(OmnomnomSMTPServer, self).__init__( (hostname, port), None)
        self.conf = conf
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        print("Peer", peer)
        print("Mailfrom", mailfrom)
        print("Rcpttos", rcpttos)
        print("Data", data)
        print("=================")

        msg = email.message_from_string(data)
        EmailProcessor.record_email(msg)
        
    @staticmethod
    def run_server(conf):
        hostname = conf.get('hostname')
        port = conf.get('port', default=25)

        db_manager.create_db(conf.get('db'))
        
        server = OmnomnomSMTPServer(hostname, port, conf)
        asyncore.loop()
        
def main():
    parser = argparse.ArgumentParser(description="Omnomnom SMTP server")
    parser.add_argument("config", nargs="?", default="/etc/omnomnom/smtpd.json",
                        help="JSON configuration file")
    args = parser.parse_args()

    config = Configuration(args.config)
    
    OmnomnomSMTPServer.run_server(config)
