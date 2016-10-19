#!/usr/bin/env python
# coding:utf-8
# 
from huobi.HuobiMain import * 
import json,urllib2
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
import urllib2,json,time,threading
from handlers.data_collection import db as d

class parameter():
    def __init__(self):
        try:
            self.ticker_ltc = json.loads(urllib2.urlopen(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js').read())
            #卖一价
            self.limit_price = self.ticker_ltc['ticker']['sell']
            #买一价
            self.buyone_price = float(self.ticker_ltc['ticker']['buy'])
            #交易总量 
            self.trade_total = self.ticker_ltc['ticker']['vol']
            # self.account_info = HuobiService.getAccountInfo(ACCOUNT_INFO)
            # self.getOrder = HuobiService.getOrders(2,GET_ORDERS)
            # #卖单数量
            # self.sellOne_count = [order for order in self.getOrder if order['type'] == 2]
            # #买单数量
            # self.buyOne_count = [order for order in self.getOrder if order['type'] == 1]
            #已完成的委托
            # self.dealOrders =  HuobiService.getNewDealOrders(2,NEW_DEAL_ORDERS)
            # #资产折合
            # self.total = float(self.account_info['total'])
            #可用资金
            # self.a_cny_display = float(self.account_info['available_cny_display'])
            # #可用莱特币
            # self.a_ltc_display = float(self.account_info['available_ltc_display'])
            #收益率
            # db = d.db_control()
            # result = db.select('SETTING',UID=0)
            # total_money = float(result[0][2])
            # db.close()
            # self.ProfitRate = '%.4f'%((self.total-total_money)/total_money*100)
        except BaseException as e:
            print u'无法获取数据',e

