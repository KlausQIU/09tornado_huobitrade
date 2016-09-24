#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
from strategy import parameter as p


class HuobiHandler(tornado.web.RequestHandler):
    def get(self):
        parameter = p.parameter()
        parameter.__init__()
        with open(os.getcwd()+'\\strategy\\test_money.txt','rb') as c:
            testMoney = c.read()  
        ProfitRate = parameter.ProfitRate
        testMoney = testMoney
        tradeTotal = parameter.trade_total
        moneyTotal = parameter.total
        self.render("index.html",ProfitRate=ProfitRate,testMoney=testMoney,tradeTotal=tradeTotal,moneyTotal=moneyTotal)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

class AccountHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class TradeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("trade.html")


