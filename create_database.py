# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
conn = sqlite3.connect('huobi.db')
# conn.execute('''CREATE TABLE trade_set
#        (ID INT PRIMARY KEY     NOT NULL,
#        NAME           TEXT    NOT NULL,
#        alias          TEXT     NOT NULL,
#        type           CHAR(50),
#        value         TEXT      NOT NULL);''')
# print "Table created successfully";

# conn.execute("INSERT INTO trade_set (ID,NAME,alias,type,value) \
#       VALUES (1, 'buy_count', '购买数量', 'Float', 1 )");
# conn.execute("INSERT INTO trade_set (ID,NAME,alias,type,value) \
#       VALUES (2, 'total_money', '投入金额', 'Float', 500 )");
# conn.execute("INSERT INTO trade_set (ID,NAME,alias,type,value) \
#       VALUES (3, 'control', '开启', 'Bool', 'True' )");
# conn.execute("INSERT INTO trade_set (ID,NAME,alias,type,value) \
#       VALUES (4, 'lastprice', '平仓价', 'Float', 'None' )");
# conn.execute("INSERT INTO trade_set (ID,NAME,alias,type,value) \
#       VALUES (5, 'lastmoney', '平仓金额', 'Float', 'None' )");

# conn.commit()
      
cursor = conn.execute("SELECT * from trade_set")
for row in cursor:
   print "ID = ", row[0]
   print "NAME = ", row[1]
   print "alias = ", row[2]
   print "type = ", row[3]
   print "value = ", row[4], "\n"
conn.close()