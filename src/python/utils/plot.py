#/usr/bin/python
#-*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    plot.py
# Version:     1.0
# Date:        2018-06-18 10:10:38
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# see: https://github.com/matplotlib/mpl_finance
from mpl_finance import candlestick_ochl as candlestick
from matplotlib.dates import num2date
from matplotlib.dates import date2num
import datetime


def plot_k_line(data):

    candlesticks = zip(date2num(data['time'].values), data['open'], data['close'], data['high'], data['low'], data['vol'])

    scale = abs(candlesticks[1][0] - candlesticks[0][0])

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylabel('Quote ($)', size=20)
    candlestick(ax, candlesticks, width=scale, colorup='g', colordown='r')

    # shift y-limits of the candlestick plot so that there is space at the bottom for the volume bar chart
    pad = 0.25
    yl = ax.get_ylim()
    ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

    # create the second axis for the volume bar-plot
    ax2 = ax.twinx()

    # set the position of ax2 so that it is short (y2=0.32) but otherwise the same size as ax
    ax2.set_position(matplotlib.transforms.Bbox([[0.125, 0.1], [0.9, 0.32]]))

    # get data from candlesticks for a bar plot
    dates = [x[0] for x in candlesticks]
    dates = np.asarray(dates)
    volume = [x[5] for x in candlesticks]
    volume = np.asarray(volume)

    # make bar plots and color differently depending on up/down for the day
    pos = data['open'] - data['close'] < 0
    neg = data['open'] - data['close'] > 0
    ax2.bar(dates[pos], volume[pos], color='green', width=scale, align='center')
    ax2.bar(dates[neg], volume[neg], color='red', width=scale, align='center')

    #scale the x-axis tight
    ax2.set_xlim(min(dates),max(dates))
    # the y-ticks for the bar were too dense, keep only every third one
    yticks = ax2.get_yticks()
    ax2.set_yticks(yticks[::3])

    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel('Volume', size=20)

    # format the x-ticks with a human-readable date.
    xt = ax.get_xticks()
    new_xticks = [num2date(d).strftime('%Y%m%d%H%M') for d in xt]
    #new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
    ax.set_xticklabels(new_xticks,rotation=45, horizontalalignment='right')

    #plt.ion()
    plt.show()

