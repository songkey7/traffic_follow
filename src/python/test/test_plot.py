#/usr/bin/python
#-*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    test_plot.py
# Version:     1.0
# Date:        2018-06-17 17:08:36
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import sys
sys.path.append('../')

from unittest import TestCase
import pandas as pd
from utils.plot import plot_k_line
import datetime


class TestPlot(TestCase):
    def test_plot_k_line(self):
        filename = 'data/data.csv'
        data = pd.read_csv(filename, sep=';')
        data['time'] = data.apply(lambda d: datetime.datetime.strptime(d['date'], '%d/%m/%Y'), axis=1)
        data['time'] = data['time'].astype(datetime.datetime)
        print data['time'].values[0]
        print type(data['time'].values[0])
        plot_k_line(data)
