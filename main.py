#!/usr/bin/env python
# coding:utf-8

import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web
from tornado.options import define, options

from url import url
from application import settings
from handlers.data_collection.profitData import ProfitDataCollection
import threading
import multiprocessing


define("port", default="7788", help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, url, **settings)

def threading_run(target,args):
    if target:
        t = threading.Thread(target=target,args=args)
        threads.append(t)

def tornadoHuobi():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.getcwd())
    threads = []
    # d = multiprocessing.Process(name='tornadoHuobi',target=tornadoHuobi)
    # n = multiprocessing.Process(name='ProfitDataCollection',target=ProfitDataCollection)
    # d.daemon = True
    # n.daemon = True
    # d.start()
    # n.start()
    # d.join()
    # n.join()
    threading_run(tornadoHuobi,()) 
    threading_run(ProfitDataCollection,())
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

#python C:\Klaus\System\16tornado_huobitrade\main.py