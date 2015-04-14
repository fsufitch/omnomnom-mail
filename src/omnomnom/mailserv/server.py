import argparse, asyncore
from smtpd import SMTPServer

from omnomnom.common.config import Configuration

class OmnomnomSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        print("Peer", peer)
        print("Mailfrom", mailfrom)
        print("Rcpttos", rcpttos)
        print("Data", data)
        print("=================")
        with open('/tmp/omnomnom_smtp.txt', 'w') as f:
            print("Peer", peer, file=f)
            print("Mailfrom", mailfrom, file=f)
            print("Rcpttos", rcpttos, file=f)
            print("Data", data, file=f)
            
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
