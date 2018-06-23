# /usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    logger.py
# Version:     1.0
# Date:        2018-06-23 07:18:15
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import logging.config


class Logger(object):
    logger = None

    def __init__(self):
        pass

    def init(self, conf, name):
        self.logger = logging.getLogger(name)
        logging.config.fileConfig(conf)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.logger.warn(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)


logger = Logger()
