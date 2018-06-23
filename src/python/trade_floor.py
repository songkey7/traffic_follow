# /usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    trade_floor.py
# Version:     1.0
# Date:        2018-06-22 21:25:46
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

from data_info import *
from exchange.huobi.huobi import ExchangeHuobi
from strategy.demo import StrategyDemo
from utils.logger import logger
from utils.plot import plot_k_line


class TradeFloor:
    def __init__(self):
        logger.init('conf/logger_config.ini', 'trade_floor')
        exchange = ExchangeHuobi(Symbol.gsc_eth)
        exchange.get_kline_from_exchange()
        exchange.get_depth_from_exchange()
        data = exchange.get_kline_series()
        plot_k_line(data)

        self.strategy = StrategyDemo()
        self.strategy.set_src_exchange(exchange)
        self.strategy.set_dst_exchange(exchange)

    def run(self):
        for cur_time, orders in self.strategy.get_orders():
            for o in orders:
                print o.type, o.price, o.vol
            self.strategy.src_exchange.set_timestamp(cur_time)
            self.strategy.src_exchange.continuous_bidding(orders)
        data = self.strategy.src_exchange.get_kline_series()
        plot_k_line(data)

if __name__ == '__main__':
    TradeFloor().run()
