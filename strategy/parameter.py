#!/usr/bin/env python
# coding:utf-8
# 
from huobi.HuobiMain import * 
import json,urllib2
from setting import *

class parameter():
    def __init__(self):
        try:
            self.ticker_ltc = json.loads(urllib2.urlopen(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js').read())
            self.account_info = HuobiService.getAccountInfo(ACCOUNT_INFO)
            self.getOrder = HuobiService.getOrders(2,GET_ORDERS)
            #卖单数量
            self.sellOne_count = [order for order in self.getOrder if order['type'] == 2]
            #买单数量
            self.buyOne_count = [order for order in self.getOrder if order['type'] == 1]
            #已完成的委托
            self.dealOrders =  HuobiService.getNewDealOrders(2,NEW_DEAL_ORDERS)
            #资产折合
            self.total = float(self.account_info['total'])
            #卖一价
            self.limit_price = self.ticker_ltc['ticker']['sell']
            #买一价
            self.buyone_price = self.ticker_ltc['ticker']['buy']
            #交易总量 
            self.trade_total = self.ticker_ltc['ticker']['vol']
            #可用资金
            self.a_cny_display = float(self.account_info['available_cny_display'])
            #可用莱特币
            self.a_ltc_display = float(self.account_info['available_ltc_display'])
            #收益率
            self.ProfitRate = '%.4f'%((self.total-total_money)/total_money*100)
        except:
            print u'无法获取数据'

if __name__ == '__main__':
    parameter = parameter()
    parameter.__init__()