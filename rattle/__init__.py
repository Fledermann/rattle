#!/usr/bin/env python3

import logging
import os
import sys

# Kind of a hack to keep flask from showing server banner.
os.environ['WERKZEUG_RUN_MAIN'] = 'true'

logger = logging.getLogger('rattle')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('(%(asctime)s) %(levelname)s: %(message)s')

# Debug log to file.
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Warnings and errors also to stderr.
logger_err = logging.StreamHandler(sys.stderr)
logger_err.setLevel(logging.WARNING)
logger_err.setFormatter(formatter)
logger.addHandler(logger_err)

# Mute verbose werkzeug log.
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)
