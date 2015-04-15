from omnomnom.common.db import manager, Email

class EmailProcessor(object):
    @staticmethod
    def get_payload_str(message):
        if not message.is_multipart():
            return message.get_payload(decode=True)
        contents = [EmailProcessor.get_payload_str(part) for part in message.get_payload()]
        return ''.join(contents)
        
    @staticmethod
    def record_email(message):
        payload = EmailProcessor.get_payload_str(message)
        payload = payload.decode()
        headers = message.items()

        print("ORIGINAL:")
        print(message)
        print("====== PAYLOAD:")
        print(payload)
        print("====== HEADERS:")

        from_addr = ""
        to_list = []
        
        for k,v in headers:
            print(k, "::", v)

        mail = Email(from_addr=message['From'],
                     to_addrs=','.join(message.get_all('To', [])),
                     subject=message['Subject'],
                     body=payload)
        
        session = manager.create_session()
        session.add(mail)
        session.commit()