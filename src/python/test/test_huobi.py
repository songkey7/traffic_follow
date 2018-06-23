# /usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    test_huobi.py
# Version:     1.0
# Date:        2018-06-17 17:08:36
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import sys

sys.path.append('../')

from unittest import TestCase
from exchange.huobi.huobi import ExchangeHuobi
from utils.plot import plot_k_line
from data_info import *
from utils.logger import logger


class TestExchangeHuobi(TestCase):
    logger.init('conf/logger_config.ini', 'trade_floor')

    def test(self):
        pass

    def test_get_kline(self):
        platform = ExchangeHuobi(Symbol.gsc_eth)
        platform.get_kline_from_exchange(5)
        data = platform.get_kline_series()
        # print data
        plot_k_line(data)

    def test_get_depth(self):
        platform = ExchangeHuobi(Symbol.gsc_eth)
        platform.get_depth_from_exchange()
        platform.print_depth(10)

    def test_load_kline_data_from_local(self):
        print ExchangeHuobi.load_kline_data_from_local('data/huobi_kline.json')

    def test_trade(self):
        platform = ExchangeHuobi(Symbol.gsc_eth)

        platform.set_order(Order(OrderType.sell, 14, 10))
        platform.set_order(Order(OrderType.sell, 13, 3))
        platform.set_order(Order(OrderType.buy, 11, 5))
        platform.set_order(Order(OrderType.buy, 10, 9))

        platform.print_depth(10)
        platform.print_kline_series()

        order_list = [Order(OrderType.buy, 13, 7), Order(OrderType.sell, 15, 8), Order(OrderType.sell, 4, 10)]
        platform.continuous_bidding(order_list)

        platform.print_depth(10)
        platform.print_kline_series()

