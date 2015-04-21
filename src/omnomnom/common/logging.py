import logging, traceback
from datetime import datetime

class VerboseFormatter(logging.Formatter):
    TEMPLATE = '[{time}] {name}/{level} :: {msg}'
    def format(self, record):
        timenow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        msg = str(record.msg)
        if record.exc_info:
            msg = self.formatException(record.exc_info)
        message = self.TEMPLATE.format(time=timenow,
                                       name=record.name,
                                       level=record.levelname,
                                       msg=msg)
        return message

    def formatException(self, exc_info):
        exc_type, exc_value, tb = exc_info
        errheader = 'EXCEPTION: {exc_name} -- {exc_message}'.format(exc_name=exc_type.__name__,
                                                                    exc_message=str(exc_value))


        traces = traceback.format_tb(tb)
        trace_lines = ''.join(traces).strip().split('\n')
        trace_lines = ['> '+line for line in trace_lines]
        final_message = '\n'.join([errheader] + trace_lines)
        return final_message

def setup_logging(log_path, debug=False):
    formatter = VerboseFormatter()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.WARNING)
    console_handler.setFormatter(formatter)

    log_handler = logging.FileHandler(log_path)
    log_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG) # level is controlled at handler level

    root_logger.handlers = []
    root_logger.addHandler(console_handler)
    root_logger.addHandler(log_handler)

    logging.getLogger('omnomnom.logging').info('set up logging; debug=%s' % bool(debug))

def log_http(request_handler):
    logger = logging.getLogger('omnomnom.webui.access')
    httprequest = request_handler.request

    log_data = {
        "method": httprequest.method,
        "uri": httprequest.uri,
        "headers": httprequest.headers,
        "client": httprequest.remote_ip,
        "full_url": httprequest.full_url(),
        "response_status": request_handler.get_status(),
    }
    
    if 400 <= request_handler.get_status() <= 499: # User error, log warning
        logger.warning(log_data)
    elif 500 <= request_handler.get_status() <= 599: # Server error, log error
        logger.error(log_data)
    else:
        logger.info(log_data)
    
    

