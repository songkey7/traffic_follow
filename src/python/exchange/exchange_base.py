# /usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    exchange_base.py
# Version:     1.0
# Date:        2018-06-18 07:36:33
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import Queue
import sys
from abc import ABCMeta, abstractmethod
from copy import deepcopy

from data_info import *
from utils.logger import logger


class ExchangeBase(object):
    __metaclass__ = ABCMeta
    _buy_list = Queue.PriorityQueue()
    _sell_list = Queue.PriorityQueue()

    def __init__(self, name, symbol, period):
        self._timestamp = time.time()
        self._name = name
        self._symbol = self.symbol(symbol)
        self._kline_series = KlineSeries(period)

    @abstractmethod
    def get_kline_from_exchange(self, period, size):
        pass

    @abstractmethod
    def get_depth_from_exchange(self):
        pass

    @abstractmethod
    def period_type(self, type):
        pass

    @abstractmethod
    def symbol(self, symbol):
        pass

    @abstractmethod
    def set_order_to_exchange(self, symbol):
        pass

    def set_timestamp(self, ts):
        self._timestamp = ts

    def get_timestamp(self):
        return self._timestamp

    def call_auction(self):
        ret_vol = 0
        ret_price = 0
        buy = self._buy_list.get()
        sell = self._sell_list.get()
        if buy.price >= sell.price:
            pass
        else:
            self._buy_list.put(buy)
            self._sell_list.put(sell)

        return ret_price, ret_vol

    def set_order_with_bidding(self, order):
        ret_vol = 0
        ret_open = close = 0
        ret_high = -sys.maxint - 1
        ret_low = sys.maxint

        if order.vol <= 0:
            return ret_vol, ret_open, close, ret_low, ret_high

        if order.type == OrderType.buy:
            if self._sell_list.empty():
                self._buy_list.put(order)
                return ret_vol, ret_open, close, ret_low, ret_high

            tmp = self._sell_list.get()
            while order.price >= tmp.price:
                if ret_vol == 0:
                    ret_open = tmp.price
                close = tmp.price
                ret_high = max(ret_high, tmp.price)
                ret_low = min(ret_low, tmp.price)
                ret_vol += min(order.vol, tmp.vol)
                if order.vol == tmp.vol:
                    return ret_vol, ret_open, close, ret_low, ret_high
                elif order.vol > tmp.vol:
                    order.vol -= tmp.vol
                    if self._sell_list.empty():
                        self._buy_list.put(order)
                        return ret_vol, ret_open, close, ret_low, ret_high
                    tmp = self._sell_list.get()
                else:
                    tmp.vol -= order.vol
                    self._sell_list.put(tmp)
                    return ret_vol, ret_open, close, ret_low, ret_high

            self._buy_list.put(order)
            self._sell_list.put(tmp)

        if order.type == OrderType.sell:
            if self._buy_list.empty():
                self._sell_list.put(order)
                return ret_vol, ret_open, close, ret_low, ret_high

            tmp = self._buy_list.get()
            while order.price <= tmp.price:
                if ret_vol == 0:
                    ret_open = tmp.price
                close = tmp.price
                ret_high = max(ret_high, tmp.price)
                ret_low = min(ret_low, tmp.price)
                ret_vol += min(order.vol, tmp.vol)
                if order.vol == tmp.vol:
                    return ret_vol, ret_open, close, ret_low, ret_high
                if order.vol > tmp.vol:
                    order.vol -= tmp.vol
                    if self._buy_list.empty():
                        self._sell_list.put(order)
                        return ret_vol, ret_open, close, ret_low, ret_high
                    tmp = self._buy_list.get()
                else:
                    tmp.vol -= order.vol
                    self._buy_list.put(tmp)
                    return ret_vol, ret_open, close, ret_low, ret_high

            self._buy_list.put(tmp)
            self._sell_list.put(order)

        return ret_vol, ret_open, close, ret_low, ret_high

    def set_order(self, order):
        if order.type == OrderType.buy:
            self._buy_list.put(order)
        if order.type == OrderType.sell:
            self._sell_list.put(order)

    def continuous_bidding(self, order_list):
        if order_list is None or len(order_list) == 0:
            return
        cur_time = self._timestamp
        ret_vol = 0
        ret_open = ret_close = 0
        ret_high = -sys.maxint - 1
        ret_low = sys.maxint

        if not self._kline_series.empty():
            ret_open = self._kline_series.last()[3]

        for i, order in enumerate(order_list):
            tmp_vol, tmp_open, tmp_close, tmp_low, tmp_high = self.set_order_with_bidding(order)
            # self.print_depth(10)
            if tmp_vol == 0:
                continue
            # TODO: open price
            if ret_open == 0:
                ret_open = tmp_open
            ret_close = tmp_close
            ret_high = max(ret_high, tmp_high)
            ret_low = min(ret_low, tmp_low)
            ret_vol += tmp_vol

        if not self._kline_series.empty():
            last_pt = self._kline_series.last()
            # TODO: to be change
            if last_pt[0] == cur_time:
                self._kline_series.pop()
                ret_vol += last_pt[1]
                ret_open = last_pt[2]
                ret_low = min(ret_low, last_pt[4])
                ret_high = max(ret_high, last_pt[5])

        self._kline_series.add(cur_time, ret_vol, ret_open, ret_close, ret_low, ret_high)

    def get_kline_series(self):
        return self._kline_series.get_data()

    def get_order_list(self):
        return self._buy_list, self._sell_list

    def print_kline_series(self):
        print self._kline_series.get_data()

    def print_depth(self, n=0):
        self.print_half_depth(self._sell_list, n if n != 0 else self._sell_list.qsize())
        self.print_half_depth(self._buy_list, n if n != 0 else self._buy_list.qsize())

    def get_sell_list_below(self, price):
        if self._sell_list.empty():
            return 0

        sell_list = self.deepcopy_order_list(self._buy_list)
        sell = sell_list.get()
        vol = 0
        while price < sell.price:
            vol += sell.vol
            sell = sell_list.get()
        return vol

    def get_buy_list_above(self, price):
        if self._buy_list.empty():
            return 0

        buy_list = self.deepcopy_order_list(self._buy_list)
        buy = buy_list.get()
        vol = 0
        while price < buy.price:
            vol += buy.vol
            buy = buy_list.get()
        return vol

    @staticmethod
    def deepcopy_order_list(order_list):
        order_list_copy = Queue.PriorityQueue()
        for x in order_list.queue:
            tmp = Order(x.type, x.price, x.vol)
            order_list_copy.put(tmp)
        return order_list_copy

    def print_half_depth(self, order_list, n):
        order_list_copy = self.deepcopy_order_list(order_list)

        array = []
        while not order_list_copy.empty():
            tmp = order_list_copy.get()
            n -= 1
            if n <= 0:
                break
            array.append(tmp)

        while len(array) > 0:
            if tmp.type == OrderType.sell:
                x = array.pop()
            else:
                x = array.pop(0)
            msg = "%s %g %d" % (x.type.name(), x.price, x.vol)
            logger.info(msg)

