#/usr/bin/python
#-*- coding:utf-8 -*-

# -------------------------------------------------------------------------------
# Filename:    test.py
# Version:     1.0
# Date:        2018-06-17 17:08:36
# Author:      songkey
# Brief:
# -------------------------------------------------------------------------------

import json
import urllib2

url_detail='https://www.huobi.com/-/x/general/index/constituent_symbol/detail?r=mt9x4osq2uc'

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'cookie':'__cfduid=d62fc0f844aa7cb52af7aa948a0e6875a1529220487; _ga=GA1.2.478540080.1529220492; _gid=GA1.2.1013783646.1529220492; gr_user_id=538be6a9-9ce3-4e71-b49c-059038d84708; SESSION=4078bd98-bbb3-45e3-aa01-dacc0ccc40d9; __zlcmid=mxhQHGOAgsvNkQ; _umdata=2BA477700510A7DF883C0B8977DC118E2844DC40CED0AEE175A42A70AC95432AF6099F3DF39276D9CD43AD3E795C914CD2E905FE2086D628AF88505BA5B286B7; HB-UC-TOKEN=%2B1CgvUD3jF9br2akjK8bmYbkoA9w3%2FQl0faKk96wd8mhXMeMaB1iv%2BU1Bhpj4O%2BAthNi%2FjowJnkH13WIFvP5RIrdQ3x20RTThL46Sq6UTXhidZG%2BaLz%2BmGjpb9bRg5a%2FKkJTYNQR%2BRDkgjDEmyrvnfoDMJ6DRjug0%2BQTR0LJDPc%3D; HB-PRO-TOKEN=8cqOZy9CxIUNEHOhrB0zciTCg914IXeIs52qK54EpPIY-uOP2m0-gvjE57ad1qDF; 8838a5745a973a12_gr_last_sent_cs1=E1C83245B79762BD30D7D36B9554966BC492ABA2ABA76BB298DB283CD5F0B37E; 8838a5745a973a12_gr_last_sent_sid_with_cs1=3797a868-cb81-4027-a7eb-edea2698b33e; 8838a5745a973a12_gr_session_id=3797a868-cb81-4027-a7eb-edea2698b33e_true; 8838a5745a973a12_gr_cs1=E1C83245B79762BD30D7D36B9554966BC492ABA2ABA76BB298DB283CD5F0B37E',
    'referer': 'https://www.huobi.com/zh-cn/etc_usdt/exchange/',
    'hb-pro-token': '8cqOZy9CxIUNEHOhrB0zciTCg914IXeIs52qK54EpPIY-uOP2m0-gvjE57ad1qDF'
}

request = urllib2.Request(url_detail, headers=headers)
res = urllib2.urlopen(request).read()
res = json.loads(res)
print res
