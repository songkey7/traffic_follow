#/usr/bin/python
#-*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    date_tools.py
# Version:     1.0
# Date:        2018-06-23 16:21:51
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import time


def cur_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())
