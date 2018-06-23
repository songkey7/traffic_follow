
from unittest import TestCase

from strategy.demo import StrategyDemo
from exchange.huobi.huobi import ExchangeHuobi
from data_info import *
from utils.logger import logger


class TestStrategyDemo(TestCase):
    logger.init('conf/logger_config.ini', 'trade_floor')

    def test_set_src_exchange(self):
        exchange = ExchangeHuobi(Symbol.gsc_eth)
        exchange.get_kline_from_exchange()
        exchange.get_depth_from_exchange()

        strategy = StrategyDemo()
        strategy.set_src_exchange(exchange)
        strategy.set_dst_exchange(exchange)
