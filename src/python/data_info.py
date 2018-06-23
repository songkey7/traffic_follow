#/usr/bin/python
#-*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    trade_floor.py
# Version:     1.0
# Date:        2018-06-18 07:36:33
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import time
import Queue
import datetime
import numpy as np
import pandas as pd
from enum import Enum


class PeriodType(Enum):
    null = 0
    min = 1
    min_5 = 2
    min_15 = 3
    min_30 = 4
    hour = 5
    day = 6
    week = 7
    month = 8
    year = 9


class Symbol(Enum):
    null = 0
    gsc_eth = 1


class OrderType(Enum):
    null = 0
    buy = 1
    sell = 2

    def name(self):
        name_dict = {
            self.sell : "sell",
            self.buy : "buy",
            self.null: "null"
        }
        return name_dict[self]


class KlineSeries:
    def __init__(self, period):
        self._schema = ['time', 'vol', 'open', 'close', 'low', 'high']
        self._data = []
        self._period_type = period

    def empty(self):
        return len(self._data) == 0

    def add(self, time, volume, open, close, low, high):
        self._data.append([time, volume, open, close, low, high])

    def pop(self):
        if self.empty():
            self._data.pop()

    def last(self):
        return [] if self.empty() else self._data[-1]

    def get_data(self):
        data = pd.DataFrame(self._data, columns=self._schema)
        data['time'] = data['time'].astype(datetime.datetime)
        data['vol'] = data['vol'].astype(np.int32)
        data[['open', 'close', 'low', 'high']] = data[['open', 'close', 'low', 'high']].astype(np.float64)
        return data


class Order(object):
    def __init__(self, type=OrderType.null, price=0.0, vol=0):
        self.type = type
        self.price = price
        self.vol = vol

    def __cmp__(self, other):
        if self.type == OrderType.buy:
            return cmp(other.price, self.price)
        else:
            return cmp(self.price, other.price)



