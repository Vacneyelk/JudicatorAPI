
import logging

japi_log = logging.getLogger('judicatorApi')
japi_log.setLevel(logging.DEBUG)

fh = logging.FileHandler('judocatorApi.log')
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
fh.setFormatter(formatter)
japi_log.addHandler(fh)