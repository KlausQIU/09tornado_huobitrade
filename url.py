#!/usr/bin/env python
# coding:utf-8

import tornado.web
import application

url = [(r"^/(favicon\.ico)", tornado.web.StaticFileHandler,
         dict(path=application.settings['static_path']))]
url += [(r"^/", "handlers.index.IndexHandler")]
url += [(r"^/huobi","handlers.huobi.HuobiHandler")]
url += [(r"^/login", "handlers.huobi.LoginHandler")]
url += [(r"^/account", "handlers.huobi.HuobiHandler")]

