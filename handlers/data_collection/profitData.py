#!/usr/bin/env python
# coding:utf-8

import tornado.web
import os
import sys
import time
import db as dbL
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from strategy import personalHandler as pH


def ProfitDataCollection():
    db = dbL.db_control()
    while True:
        users = db.select('user')
        print users
        for user in users:
            if len(user[4]) == 32 and len(user[5]) == 32:
                personalH = pH.personalHandler(user[4].encode('utf-8'),user[5].encode('utf-8'))
                profitData = db.select('profitData',uid=user[1])
                setting = db.select('SETTING',UID=user[1])
                count = max([item[0] for item in profitData])+1 if profitData else 0
                profit = personalH.profit
                db.insert('profitData',count,time.strftime('%Y%m%d%H%M%S',time.localtime()),setting[0][0],setting[0][0],profit)
            else:
                pass
        time.sleep(900)
        continue

if __name__ == '__main__':
    ProfitDataCollection()