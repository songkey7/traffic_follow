# /usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    demo.py
# Version:     1.0
# Date:        2018-06-22 21:32:46
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

from abc import ABCMeta, abstractmethod

from data_info import *


class StrategyBase(object):
    __metaclass__ = ABCMeta

    src_exchange = None
    dst_exchange = None

    @abstractmethod
    def get_orders(self):
        pass

    def set_src_exchange(self, exchange):
        self.src_exchange = exchange
        self.src_exchange.get_depth_from_exchange()
        self.src_exchange.get_kline_from_exchange()

    def set_dst_exchange(self, exchange):
        self.dst_exchange = exchange
        self.dst_exchange.get_depth_from_exchange()
        self.dst_exchange.get_kline_from_exchange()
