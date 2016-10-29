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
        # try:
            #个人信息
            self.account_info = HuobiService.getAccountInfo(ACCOUNT_INFO,access_key,secret_key)
            #委托单信息
            self.getOrder = HuobiService.getOrders(2,GET_ORDERS,access_key,secret_key)
            #借用的杠杆币
            self.loan_ltc_display = float(self.account_info['loan_ltc_display']) if self.account_info.has_key('loan_ltc_display') else 0
            self.ltc_total = float(self.account_info['available_ltc_display'])+float(self.account_info['frozen_ltc_display'])
            #全部的财产
            self.total = self.account_info['total']
            #净值(即除开杠杆)
            self.net_asset = float(self.account_info['net_asset'])
            #akey
            self.a_key = access_key
            #skey
            self.s_key = secret_key
            #收益
            self.profit = self.Profit()
            #当前仓位
            self.freightSpace = '%.2f'%(self.freightSpace())
        # except BaseException as e:
        #     self.total = 0
        #     self.profit = 0
        #     self.getOrder = {}
        #     self.net_asset = 0
        #     self.loan_ltc_display = 0
        #     print e


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
        db.close()
        profit = '%.2f'%(float(self.net_asset)-float(setting[0][2]))
        return profit
        
    def freightSpace(self):
        parameter = p.parameter()
        parameter.__init__()
        result = (parameter.buyone_price*self.ltc_total)/self.net_asset
        return result

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
            print e
            return {}

if __name__ == '__main__':
    p = personalHandler('7ffd4f94-63d605e6-d5f400fb-a6ba0', 'd5d52f33-dcbd2167-5c6b7b0f-f5676')
    print p.freightSpace

