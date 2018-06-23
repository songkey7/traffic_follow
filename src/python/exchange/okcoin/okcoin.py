# /usr/bin/python
# -*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    okcoin.py
# Version:     1.0
# Date:        2018-06-18 09:07:56
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import sys
sys.path.append('../')

from platform_base import PlatformBase
from OkcoinSpotAPI import *
import datetime


class ExchangeOKCoin(PlatformBase):
    apikey = '044f7c4e-02d9-422a-bf99-e7993d51400d'
    secretkey = '6332DBB3220E056A117AECAF5D2CC2A2'
    okcoinRESTURL = 'www.okcoin.com'   #请求注意：国内账号需要 修改为 www.okcoin.cn

    def __init__(self, symbol):
        super(ExchangeOKCoin, self).__init__('huobi', symbol)

    def get_kline(self, period, size):
        okcoinSpot = OKCoinSpot(self.okcoinRESTURL, self.apikey, self.secretkey)
        res = get_kline(self._symbol, period, size)
        print res
        if 'status' in res and res['status'] == 'ok':
            for d in res['data']:
                self._kline_series.add(datetime.datetime.fromtimestamp(int(d['id'])),
                                       d['amount'], d['open'], d['close'], d['low'], d['high'])
        return self._kline_series.get_data()

    def get_depth(self, type):
        return get_depth(self._symbol, type)
