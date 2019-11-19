

import logging

logger = logging.getLogger('test_log')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
a = [1, 2, 3]
logger.info(f'My list: {a}')
logger.error('Big Error')

