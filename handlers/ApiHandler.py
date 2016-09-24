#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver  
import tornado.ioloop  
import tornado.options  
import tornado.escape
import json
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
import urllib2,json,time,threading
from datetime import datetime 
from strategy import parameter as p

__author__ = 'KlausQiu'

class ProfitHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

  
class TradeHandler(tornado.web.RequestHandler):  
    def get(self):
        parameter = p.parameter()
        parameter.__init__()
        with open(os.getcwd()+'/strategy/test_money.txt','rb') as c:
            testMoney = c.read()  
        respon = {
        'ProfitRate' : parameter.ProfitRate,
        'testMoney' : testMoney,
        'tradeTotal' : parameter.trade_total,
        'moneyTotal' : parameter.total  
        }
        respon_json = tornado.escape.json_encode(respon) 
        self.write(respon_json)


class totalHandler(tornado.web.RequestHandler):  
    def get(self):
        ltc_trade = huobi_trade.ltc_trade()
        ltc_trade.__init__()  
        respon = {
        'ProfitRate' : ltc_trade.ProfitRate,
        'testMoney' : ltc_trade.testMoney,
        'tradeTotal' : ltc_trade.trade_total,
        'moneyTotal' : ltc_trade.total  
        }
        respon_json = tornado.escape.json_encode(respon)  
        self.write(respon_json)