#!/usr/bin/env python
# coding:utf-8

import tornado.web
import db
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from strategy import parameter as p
from strategy.setting import total_money


if __name__ == '__main__':
    db = db.db_control()
    p = p.parameter()
    #db.creatTable('SETTING','UID INTEGER PRIMARY KEY','TESTMONEY BLOB','TOTALMONEY BLOB','BUYCOUNT BLOB','overHighPrice BLOB','overLowPrice BLOB','COEFFICIENT BLOB','lastPrice BLOB')
    #db.insert('SETTING', 0,688.121,700,1,27,25,0.985,0)
    #db.insert('SETTING', 1,0,0,1,27,25,0.985,0)
    #db.delete('SETTING')
    # d1 = {'TESTMONEY':701.0}
    # d2 = {'UID':0}
    # db.update('SETTING',d1,d2)
    # d = db.select('SETTING')
    # print d
