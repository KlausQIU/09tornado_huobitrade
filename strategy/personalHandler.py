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
from strategy.huobi import HuobiService
import operator
from strategy import parameter as p

__author__ = 'KlausQiu'

class personalHandler():
    """docstring for personalHandler /for personal accountInfo handler,make some parameter"""
    def __init__(self,access_key,secret_key):
        try:
            self.account_info = HuobiService.getAccountInfo(ACCOUNT_INFO,access_key,secret_key)
            self.getOrder = HuobiService.getOrders(2,GET_ORDERS,access_key,secret_key)
            self.loan_ltc_display = float(self.account_info['loan_ltc_display'])
            self.total = self.account_info['total']
            self.net_asset = float(self.account_info['net_asset'])
            self.a_key = access_key
            self.s_key = secret_key
            self.profit = self.Profit()
        except BaseException as e:
            self.total = 0
            self.profit = 0
            self.getOrder = {}
            self.net_asset = 0
            print e


    def ProfitRate(self,uid):
        parameter = p.parameter()
        parameter.__init__()
        db = d.db_control()
        result = db.select('SETTING',UID=uid)
        self.total_money = float(result[0][2])
        db.close()
        self.ProfitRate = '%.4f'%((self.net_asset-self.total_money)/self.total_money*100) if self.total_money !=0 else 0
        return self.ProfitRate

    def Profit(self):
        parameter = p.parameter()
        parameter.__init__()
        db = d.db_control()
        user = db.select('user',access_key=self.a_key)
        setting = db.select('SETTING',UID = user[0][1])
        profit = '%.2f'%(float(self.net_asset)-float(setting[0][2]))
        print setting[0][2]
        print profit
        return profit
        

    def CancelOrder(self,coinType,id):
        try:
            result = HuobiService.cancelOrder(coinType, id, CANCEL_ORDER, self.a_key, self.s_key)
            if result.has_key('result'):
                return result
            else:
                return {'result':'fail'}
        except BaseException as e:
            print u'cancel order detect trouble!!',e

    def DealOrder(self,coinType):
        try:
            result = HuobiService.getNewDealOrders(coinType, NEW_DEAL_ORDERS, self.a_key,self.s_key)
            if result:
                result.sort(key=operator.itemgetter('last_processed_time'),reverse=True)  
                return result
            else:
                return {'result':'fail'}
        except BaseException as e:
            return {}

