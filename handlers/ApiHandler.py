#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver  
import tornado.ioloop  
import tornado.options  
import tornado.escape
import tornado.websocket
import json
import sys
import os
import tornado.ioloop
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
import urllib2,json,time,threading
from datetime import datetime 
from strategy import parameter as p
from strategy import personalHandler as pH
from handlers.data_collection import db as d

__author__ = 'KlausQiu'


class BaseWebSocketHandler(tornado.websocket.WebSocketHandler):
    def baseOpenDb(self):
        parameter = p.parameter()
        parameter.__init__()
        db = d.db_control()
        username = tornado.escape.utf8(self.get_secure_cookie('user'))
        return db,username

    def on_close(self):
        print "WebSocket closed"

class ProfitHandler(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print "ProfitHandler websocket open"
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        result = db.select('profitData',uid=result[0][1])
        db.close()
        if len(result) > 20:
            result = result[-200:]
        respon_json = tornado.escape.json_encode(result) 
        self.write_message(respon_json)
        self.on_close()
  
class accountInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print "AccountInfo websocket open"
        db,username = self.baseOpenDb()
        parameter = p.parameter()
        result = db.select('user',name = username)
        personalH = pH.personalHandler(result[0][4],result[0][5])
        ProfitRate = personalH.ProfitRate(result[0][1])
        result = db.select('SETTING',UID=result[0][1])
        testMoney = result[0][1]
        respon = {
        'ProfitRate' : ProfitRate,
        'testMoney' : testMoney,
        'tradeTotal' : parameter.trade_total,
        'net_asset' : personalH.net_asset,
        'moneyTotal':personalH.total,
        'loan_ltc_display':personalH.loan_ltc_display
        }
        respon_json = tornado.escape.json_encode(respon)
        self.write_message(respon_json)
        self.on_close()

class APIInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'APIInfo has been opened'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            ACCESS_KEY=result[0][4]
            SECRET_KEY=result[0][5]
            SettingResult = db.select('SETTING',UID = result[0][1])
            result = {'access_key':ACCESS_KEY,'secret_key':SECRET_KEY,'TOTALMONEY':SettingResult[0][2]}
            respon_json = tornado.escape.json_encode(result)
            self.write_message(respon_json)
            self.on_close()

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            selectRow = {'name':username}
            message = json.loads(message)
            UResult = db.select('user',name = username)
            userRow = {key:message[key] for key in ['access_key','secret_key']} 
            UserResult = db.update("user",userRow,selectRow)
            setRow = {key:message[key] for key in ['TOTALMONEY']}
            setselect = {'UID':UResult[0][1]}
            SetResult = db.update("SETTING",setRow,setselect)
            if UserResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(UserResult)
                self.write_message(respon_json)
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()


class entrustInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print "entrustInfo websocket Open"
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            getOrders = personalH.getOrder
            respon_json = tornado.escape.json_encode(getOrders)
            self.write_message(respon_json)
            self.on_close()
        
class entrustCancel(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'cancel Order websocket Open'

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            oid = int(message)
            result = personalH.CancelOrder(2,oid)
            respon_json = tornado.escape.json_encode(result)
            self.write_message(respon_json)
            self.on_close()

class tradeSetting(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'tradeSetting Order websocket Open'

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            message = json.loads(message)
            selectRow = {'UID':result[0][1]}
            SettingResult = db.update("SETTING",message,selectRow)
            if SettingResult['msg'] == 'success':
                result = db.select('SETTING',UID = result[0][1])
                result = {'testMoney':result[0][1]}
                respon_json = tornado.escape.json_encode(result)
                self.write_message(respon_json)
                self.on_close()

class tradeSetInfo(BaseWebSocketHandler):
    clients = set()  
    def open(self):
        print 'tradeSetInfo Order websocket Open'

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            selectRow = {'UID':result[0][1]}
            result = db.select('SETTING',UID = result[0][1])
            result = {'testMoney':result[0][1],'highPrice':result[0][4],'lowPrice':result[0][5]}
            respon_json = tornado.escape.json_encode(result)
            self.write_message(respon_json)
            self.on_close()

class dealMessage(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'dealMessage wesocket Open'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            personalH = pH.personalHandler(result[0][4],result[0][5])
            dealOrders = personalH.DealOrder(2) if personalH.DealOrder(2) else {}
            respon_json = tornado.escape.json_encode(dealOrders)
            self.write_message(respon_json)
            self.on_close()


class avatarInfo(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'avatarInfo websocket Open'
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            avatarInfo = {"name":result[0][2],"password":result[0][3]}
            respon_json = tornado.escape.json_encode(avatarInfo)
            self.write_message(respon_json)
            self.on_close()

    def on_message(self, message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            userRow = {'name':message['name'],'password':message['password']}
            selectRow = {'UID':result[0][1]}
            UserResult = db.update("user",userRow,selectRow)
            if UserResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(userRow)
                self.write_message(respon_json)
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()

class gridSetApi(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'gridSetApi websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            message = ','.join(message)
            updateRow = {'position':message}
            selectRow = {'UID':result[0][1]}
            FResult = db.update("fibonacciGrid",updateRow,selectRow)
            if FResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(FResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()


class tradePennySetHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'tradePennySetHandler websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            print message
            updateRow = message
            selectRow = {'UID':result[0][1]}
            SResult = db.update("SETTING",updateRow,selectRow)
            print SResult
            if SResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(SResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()
        

class tradeOrderSetHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'tradeOrderSetHandler websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            print message
            updateRow = {'PriceDict':str(message)}
            selectRow = {'UID':result[0][1]}
            SResult = db.update("SETTING",updateRow,selectRow)
            print SResult
            if SResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(SResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()

class tradePennyShow(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'tradePennyShow websocket Open'

    def on_message(self,message):
        db,username = self.baseOpenDb()
        result = db.select('user',name = username)
        if result:
            message = json.loads(message)
            print message
            updateRow = {'PriceDict':str(message)}
            selectRow = {'UID':result[0][1]}
            SResult = db.update("SETTING",updateRow,selectRow)
            print SResult
            if SResult['msg'] == 'success':
                respon_json = tornado.escape.json_encode(SResult)
                self.write_message(respon_json)
                self.on_close()
            else:
                result = tornado.escape.json_encode({'msg':'fail'})
                self.write_message(result)
                self.on_close()

class ltcDataHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'ltcDataHandler websocket Open'
        ticker_ltc = json.loads(urllib2.urlopen(r'http://api.huobi.com/staticmarket/ticker_ltc_json.js').read())
        respon_json = tornado.escape.json_encode(ticker_ltc)
        self.write_message(respon_json)

class btcDataHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'btcDataHandler websocket Open'
        ticker_ltc = json.loads(urllib2.urlopen(r'http://api.huobi.com/staticmarket/ticker_btc_json.js').read())
        respon_json = tornado.escape.json_encode(ticker_ltc)
        self.write_message(respon_json)


class handlerltcHandler(BaseWebSocketHandler):
    clients = set()
    def open(self):
        print 'handlerltcHandler websocket Open'
        handlerltc = json.loads(urllib2.urlopen(r'http://api.huobi.com/staticmarket/ltc_kline_015_json.js').read())
        handlerltc = handlerltc[-200:]
        respon_json = tornado.escape.json_encode(handlerltc)
        self.write_message(respon_json)

        # var handlerltcUrl = 'ws://'+window.location.host+'/api/handlerltc'
        # var handlerltcws = new WebSocket(handlerltcUrl);
        # handlerltcws.onmessage = function(event){
        # var data = JSON.parse(event.data);
        # data0 = splitData(data);
        # handlerltcws.close();
        # }