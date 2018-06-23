# /usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    huobi.py
# Version:     1.0
# Date:        2018-06-18 09:07:56
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import datetime
import json

from data_info import *
from utils import date_tools
from ..exchange_base import ExchangeBase
import HuobiService


class ExchangeHuobi(ExchangeBase):
    def __init__(self, symbol, period=PeriodType.min):
        super(ExchangeHuobi, self).__init__('huobi', symbol, period)

    @staticmethod
    def load_kline_data_from_local(filename):
        with open(filename) as fin:
            line = fin.read()
            res = json.loads(line)
            return res

    @staticmethod
    def load_depth_data_from_local(filename):
        with open(filename) as fin:
            line = fin.read()
            res = json.loads(line)
            return res

    @staticmethod
    def symbol(symbol):
        symbol_map = {
            Symbol.gsc_eth: 'gcseth'
        }
        print symbol
        return symbol_map[symbol]

    @staticmethod
    def period_type(type):
        period_type_map = {
            PeriodType.min: '1min',
            PeriodType.min_5: '5min',
            PeriodType.min_15: '15min',
            PeriodType.min_30: '30min',
            PeriodType.hour: '60min',
            PeriodType.day: '1day',
            PeriodType.week: '1week',
            PeriodType.month: '1mon',
            PeriodType.year: '1year'
        }
        return period_type_map[type]

    def set_order_to_exchange(self, symbol):
        raise NotImplementedError

    def get_data_to_local(self, path, size=120):
        res = HuobiService.get_kline(self._symbol, self.period_type(self._kline_series._period_type), size)
        print res
        kline_file = '%s/huobi_kline_%s.json' % (path, date_tools.cur_time())
        fout = open(kline_file, 'w')
        fout.write(json.dumps(res))

        res = HuobiService.get_depth(self._symbol, 'step0')
        print res
        depth_file = '%s/huobi_deep_%s.json' % (path, date_tools.cur_time())
        fout = open(depth_file, 'w')
        fout.write(json.dumps(res))

    def get_kline_from_exchange(self, size=120):
        # res = HuobiService.get_kline(self._symbol, self.period_type(self._kline_series._period_type), size)
        res = self.load_kline_data_from_local('data/huobi_kline.json')

        if 'status' in res and res['status'] == 'ok':
            for d in reversed(res['data']):
                self._kline_series.add(datetime.datetime.fromtimestamp(int(d['id'])),
                                       d['amount'], d['open'], d['close'], d['low'], d['high'])

    def get_depth_from_exchange(self):
        # HuobiService.get_depth(self._symbol, 'step0')
        res = self.load_depth_data_from_local('data/huobi_depth.json')

        if 'status' in res and res['status'] == 'ok' and 'tick' in res:
            if 'ts' in res['tick']:
                self.set_timestamp(float(res['tick']['ts']) / 1000)
            else:
                self.set_timestamp()

            for bid in res['tick']['bids']:
                self.set_order(Order(OrderType.buy, bid[0], bid[1]))
            for ask in res['tick']['asks']:
                self.set_order(Order(OrderType.sell, ask[0], ask[1]))
