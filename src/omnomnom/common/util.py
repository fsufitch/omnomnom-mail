import re

class EmailUtil(object):
    MIME_REGEX = re.compile('^([^;]*)(?:;.*charset=([^;]*)(?:;|$)?)?')
    @staticmethod
    def parse_mime(mime, default=('text/plain', 'utf-8')):
        if not mime:
            return default
        mime = mime.strip().lower()
        match = EmailUtil.MIME_REGEX.search(mime)
        content_type, encoding = match.groups() if match else (None, None)
        content_type = (content_type or default[0]).lower()
        encoding = (encoding or default[1]).lower()
        return content_type, encoding

    @staticmethod
    def render_to_original(msg):
        return msg.as_string()

    @staticmethod
    def render_content(msg, allow_html=False):
        content_type, encoding = EmailUtil.parse_mime(msg.get('Content-Type'))
        if not 'multipart' in content_type:
            if content_type.startswith('text'):
                logger.debug('Rendered message as: %s/%s' % (content_type, encoding))
                return msg.get_payload(decode=True).decode(encoding)
            else:
                return '[[Omnomnom :: Unknown content type: %s]]' % content_type

        content = ''
        if ('mixed' in content_type or
            'digest' in content_type or
            'parallel' in content_type):
            # These types have sequential message reading
            for sub_msg in msg.get_payload():
                content += EmailUtil.render_content(sub_msg, allow_html=allow_html)

        elif 'alternative' in content_type:
            # Choose based on their content types
            chosen_msg = None
            for sub_msg in msg.get_payload():
                logger.debug('Sub-message:')
                logger.debug(sub_msg)
                sub_mime = EmailUtil.parse_mime(sub_msg.get('Content-Type'))
                sub_type, sub_enc = sub_mime
                if sub_type == 'text/plain':
                    if not allow_html or not chosen_msg:
                        # Allow overriding HTML if HTML is disallowed
                        # Otherwise, only use plain text if nothing else is available
                        chosen_msg = sub_msg
                if allow_html and ('html' in sub_type):
                    chosen_msg = sub_msg
            if chosen_msg:
                content = EmailUtil.render_content(sub_msg, allow_html=allow_html)
            else:
                content = "[[Omnomnom :: no viable multipart content type found]]"
        return content
            