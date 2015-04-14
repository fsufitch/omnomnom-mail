import argparse, asyncore, email
from smtpd import SMTPServer

from omnomnom.common.config import Configuration

class OmnomnomSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print("Peer", peer)
        print("Mailfrom", mailfrom)
        print("Rcpttos", rcpttos)
        print("Data", data)
        print("=================")

        mail = email.message_from_string(data)
        for key in mail.keys():
            print(key, "::", mail.get(key))
        print(mail.get_payload())
            
    @staticmethod
    def run_server(conf):
        hostname = conf.get('hostname')
        port = conf.get('port', default=25)

        server = OmnomnomSMTPServer( (hostname, port), None)

        asyncore.loop()
        
        
def main():
    parser = argparse.ArgumentParser(description="Omnomnom SMTP server")
    parser.add_argument("config", nargs="?", default="/etc/omnomnom/smtpd.json",
                        help="JSON configuration file")
    args = parser.parse_args()

    config = Configuration(args.config)
    
    OmnomnomSMTPServer.run_server(config)
