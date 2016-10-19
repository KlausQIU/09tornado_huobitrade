# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 
import sqlite3
import os
import sys

class db_control():
    def __init__(self):
        self.cx = sqlite3.connect(r'C:\Klaus\System\16tornado_huobitrade\huobi.db')
        self.cursor = self.cx.cursor()

    def creatTable(self,tableName,*args):
        sql = 'create table '
        sql += tableName
        field = ''
        for value in args:
            if value == args[-1]:
                field += value
            else:
                field += value+','
        field = '(' + field + ')' 
        sql += field
        try:
            self.cursor.execute(sql)
            self.cx.commit()
            print u'new table %s has been build'%tableName
            self.cursor.close()
            self.cx.close()
        except BaseException as e:
            print u'Error:',e

    def insert(self,tableName,*args):
        sql = 'insert into '+tableName+' values('
        field = ''
        for index in range(0,len(args)-1):
            if type(args[index]) != int or type(args[index]) != float :
                field += "'%s'"%args[index]+',' 
            else:
                field += '%s'%args[index]+','
        field += "'%s'"%args[len(args)-1]
        field = field + ')' 
        sql += field
        try:
            self.cursor.execute(sql)
            self.cx.commit()
            print u'new data %s has been insert'%args
            self.cursor.close()
            self.cx.close()
        except BaseException as e:
            print u'Error:',e

    def select(self,tableName,*args,**kw):
        sql = 'select '
        if args:
            for value in args:
                sql += value if value == args[-1] else value+','
            sql += 'from '+ tableName
        else:
            sql += '* from '+tableName
        if kw:
            for key in kw:
                sql += ' where %s'%key + '=' + '"%s"'%kw[key]
        result = self.cursor.execute(sql)
        rowlist = []
        for row in result:
            if len(row) == 0:
                return []
            rowlist.append(list(row))
        return rowlist
        

    def delete(self,tableName,**kw):
        sql = "DELETE from "+tableName +' where '
        if kw:
            print len(kw)
            if len(kw) == 1:
                for key in kw:
                    sql += key + '=' + ('%s' if type(kw[key]) == int else '"%s"')%kw[key] 
            else:
                for key in kw:
                    sql += key + '=' + ('%s' if type(kw[key]) == int else '"%s"')%kw[key] + ' and '
                sql = sql[:-4]
            try:   
                self.cursor.execute(sql)
                self.cx.commit()
                print u'delete success'
                self.cursor.close()
                self.cx.close()
            except:
                print u'delete fail'
        else:
            sql = 'drop table '+tableName
            try: 
                self.cursor.execute(sql)
                self.cx.commit()
                self.cursor.close()
                self.cx.close()
                print u'delete %s success'%tableName
            except:
                print u'delete %s fail'%tableName

    def update(self,tableName,updateRow,selectRow):
        sql = 'update '+tableName+' set '
        for key in updateRow:
            sql += key + '=' + ('%s' if type(updateRow[key]) == int else '"%s"')%updateRow[key] + ','
        sql = sql[:-1]
        sql += 'where '
        for key in selectRow:
            sql += key + '=' + ('%s' if type(selectRow[key]) == int else '"%s"')%selectRow[key] + ' and '
        sql = sql[:-4]
        try:   
            self.cursor.execute(sql)
            self.cx.commit()
            print u'update success'
            return {'msg':'success'}
            self.cursor.close()
            self.cx.close()
        except BaseException as e:
            print u'update fail',e
            return {'msg':['fail',e]}

    def close(self):
        try:
            self.cursor.close()
            self.cx.close()
        except:
            print u'close Error'


if __name__ == '__main__':
    db = db_control()
    #db.creatTable('profitData','NO INTEGER','Time BLOB','id integer','uid integer','Profit BLOB')
    #db.creatTable('fibonacciGrid','id integer','uid integer','position')
    #db.insert('fibonacciGrid',1,1,'0.1,0.3,0.5,0.6,0.8,0.9')
    #db.delete('fibonacciGrid')
    print db.select('fibonacciGrid')
    #print db.select('user')
    #db.creatTable('user','id integer primary key','uid integer','name varchar(10) UNIQUE','password TEXT','access_key text UNIQUE','secret_key text UNIQUE')
    #db.insert('user',0,0,'Moon','qiu','7ffd4f94-63d605e6-d5f400fb-a6ba0','d5d52f33-dcbd2167-5c6b7b0f-f5676')
    # db.insert('user',1,1,'xuan','huang','11111111111','222222222222')
    #d1 = {'access_key':'1201110a-db609c49-0761f29f-5416b'}
    # d1 = {'secret_key':'f9eb3f82-e09da827-5ace3f4c-57390'}
    # d1 = {'name':'Moon','password':'qiu'}
    # d2 = {'id':0}
    # db.update('user',d1,d2)
    # c = db.select('user')
    # print c
    # db.close()
    # db.delete('huobi',id=1,name='MoonQiu')
    #db.insert('huobi',0,0,'KlausQiu','qiu','11111111111111','2222222222222')
    #db.creatTable('huobi','id integer primary key','uid integer','name varchar(10) UNIQUE','password TEXT','access_key text UNIQUE','secret_key text UNIQUE')
    