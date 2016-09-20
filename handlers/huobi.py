#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.web


class HuobiHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

class AccountHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
