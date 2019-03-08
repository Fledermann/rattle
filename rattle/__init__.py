#!/usr/bin/env python3

import logging

logger = logging.getLogger('rattle')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                              '%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
