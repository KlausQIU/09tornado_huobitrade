#!/usr/bin/env python
# coding:utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web
from tornado.options import define, options

from url import url
from application import settings

define("port", default="7788", help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url, **settings)

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.getcwd())
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

#python C:\Klaus\System\16tornado_huobitrade\main.py