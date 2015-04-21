from omnomnom.common.logging import setup_logging
setup_logging('foo.txt')

import logging
logging.debug('this is a debug message')
logging.info('stuff is working')
logging.warning('look out behind you!')
logging.error('oh crap it\'s broken')
logging.critical('everything sucks')

try:
    x = 1/0

except Exception as e:
    logging.exception(e)
