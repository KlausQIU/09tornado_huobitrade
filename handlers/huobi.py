#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web
import sys
import os
append_path =  os.path.dirname(os.getcwd())
sys.path.append(append_path)
from strategy import parameter as p
from handlers.data_collection import db as d
import time
from strategy import personalHandler as pH
from strategy.grid import fibonacci  as f

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class HuobiHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        username = tornado.escape.xhtml_escape(self.current_user)
        db = d.db_control()
        result = db.select('user',name = username)
        if result:
            SettingResult = db.select('SETTING',UID=result[0][1])
            personalH = pH.personalHandler(result[0][4],result[0][5])
            getOrders = personalH.getOrder if personalH.getOrder else {}
            dealOrders = personalH.DealOrder(2) if personalH.DealOrder(2) else {}
            mount=' ' if len(getOrders) == 0 else '('+'%s'%(len(getOrders))+')'
            self.render("index.html",orders=getOrders,mount=mount,dealOrders=dealOrders,user=result)
        else:
            self.redirect('login')

    def post(self):
        db = d.db_control()
        access_key = self.get_argument("access_key")
        secret_key = self.get_argument("secret_key")
        username = tornado.escape.xhtml_escape(self.current_user)
        if username:
            updateRow = {'access_key':access_key,'secret_key':secret_key}
            selectRow = {'name':username}
            db.update("user",updateRow,selectRow)
            result = db.select('user',name = username)
            if result:
                SettingResult = db.select('SETTING',UID=result[0][1])
                testMoney = SettingResult[0][1]
                personalH = pH.personalHandler(result[0][4],result[0][5])
                getOrders = personalH.getOrder if personalH.getOrder else {}
                dealOrders = personalH.DealOrder(2)
                mount=' ' if len(getOrders) == 0 else '('+'%s'%(len(getOrders))+')'
            self.render("index.html",ACCESS_KEY=result[0][4],SECRET_KEY=result[0][5],orders=getOrders,mount=mount,dealOrders=dealOrders)
        else:
            self.redirect('login')

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("Password")
        self.set_secure_cookie("user", self.get_argument("username")) 
        db = d.db_control()
        result = db.select('user',name = username)
        if result:
            if result[0][3] == password:  
                self.redirect("main")
            else:
                self.render('login.html',errorMessage="Incorrect Password")
        else:
            self.render('login.html',errorMessage="Incorrect Name")
         

class TradeHandler(BaseHandler):
    def get(self):
        self.render("trade.html")


class entrustHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        username = tornado.escape.xhtml_escape(self.current_user)
        db = d.db_control()
        result = db.select('user',name = username)
        if result:
            ACCESS_KEY=result[0][4]
            SECRET_KEY=result[0][5]
            personalH = pH.personalHandler(result[0][4],result[0][5])
            getOrders = personalH.getOrder if personalH.getOrder else {}
            if getOrders:
                self.render("component/entrust_message.html",orders=getOrders)


class LogoutHandler(BaseHandler):  
    def get(self):  
        username = tornado.escape.xhtml_escape(self.current_user)
        self.clear_cookie("user",username)  
        self.redirect("/login")  


class gridHandler(BaseHandler):

    @tornado.web.authenticated  
    def get(self):  
        if not self.current_user:
            self.redirect("/login")
            return
        username = tornado.escape.xhtml_escape(self.current_user)
        db = d.db_control()
        result = db.select('user',name = username)
        if result:
            fibonacci = f(result[0][1])
            fResult = fibonacci.fibonacciResult
            self.render("gridBase.html",user=result,fibonacci=fResult)
        else:
            self.redirect('login')

    @tornado.web.authenticated
    def post(self):
        if not self.current_user:
            self.redirect("/login")
            return
        username = tornado.escape.xhtml_escape(self.current_user)
        db = d.db_control()
        result = db.select('user',name = username)
        if result:
            
            fibonacci = f(result[0][1])
            fResult = fibonacci.fibonacciResult
            self.render("gridBase.html",user=result,fibonacci=fResult)
        else:
            self.redirect('login')

