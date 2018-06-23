#/usr/bin/python
#-*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    strategy_base.py
# Version:     1.0
# Date:        2018-06-22 21:32:46
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

from copy import deepcopy

from strategy_base import StrategyBase
from data_info import *
import random


class StrategyDemo(StrategyBase):
    def __init__(self):
        super(StrategyDemo, self).__init__()
        target_vol = 100000

    def set_src_exchange(self, exchange):
        self.src_exchange = deepcopy(exchange)
        data = self.src_exchange._kline_series._data
        self.src_exchange._kline_series._data = data[:len(data)/2]
        self.src_exchange.print_kline_series()
        self.src_exchange.print_depth(10)

    def set_dst_exchange(self, exchange):
        self.dst_exchange = exchange
        data = self.dst_exchange._kline_series._data
        self.dst_exchange._kline_series._data = data[len(data)/2:]
        self.dst_exchange.print_kline_series()
        self.dst_exchange.print_depth(10)

    def get_orders(self):
        kline = self.dst_exchange.get_kline_series()
        for i, row in kline.iterrows():
            ret = []
            target_price = row['close']
            cur_time = row['time']
            target_vol = int(10000 * random.random()) + 50000
            delta_vol = int(10000 * random.random())
            vol1 = self.src_exchange.get_sell_list_below(target_price)
            vol2 = self.src_exchange.get_buy_list_above(target_price)
            if vol1 > 0:
                if vol1 >= target_vol:
                    ret.append(Order(OrderType.buy, target_price, vol1 + delta_vol))
                else:
                    ret.append(Order(OrderType.buy, target_price, target_vol + delta_vol))
                    ret.append(Order(OrderType.sell, target_price, target_vol - vol1))
            elif vol2 > 0:
                if vol2 >= target_vol:
                    ret.append(Order(OrderType.sell, target_price, vol2))
                else:
                    ret.append(Order(OrderType.sell, target_price, target_vol + delta_vol))
                    ret.append(Order(OrderType.buy, target_price, target_vol - vol2))
            else:
                ret.append(Order(OrderType.sell, target_price, target_vol + delta_vol))
                ret.append(Order(OrderType.buy, target_price, target_vol))

            yield cur_time, ret

