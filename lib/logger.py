import logging

import main

logging.basicConfig(filename='cloud_functions.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')