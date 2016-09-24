# !/usr/bin/env python
# -*- coding:utf-8 -*-
# 
import sqlite3
import os
import sys

class db_control():
    def __init__(self):
        self.cx = sqlite3.connect('huobi.db')
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
        print sql
        try:
            self.cursor.execute(sql)
            self.cx.commit()
            self.cursor.close()
            self.cx.close()
            print u'new table %s has been build'%tableName
        except BaseException as e:
            print u'Error:',e

    def insert(self,tableName,*args):
        sql = 'insert into '+tableName+' values('
        field = ''
        for value in args:
            if value == args[-1]:
                field += "'%s'"%value
            elif type(value) != int:
                field += "'%s'"%value+','
            else:
                field += '%s'%value+','
        field = field + ')' 
        sql += field
        print sql
        try:
            self.cursor.execute(sql)
            self.cx.commit()
            self.cursor.close()
            self.cx.close()
            print u'new data %s has been insert'%args
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
                sql += ' where %s'%key + '=' + '%s'%kw[key]
        result = self.cursor.execute(sql)
        dictresult = {}
        for row in result:
            rowlist = []
            for i in range(1,6):
                rowlist.append(row[i])
            dictresult[row[0]] = rowlist
        return dictresult

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
                self.cursor.close()
                self.cx.close()
                print u'delete success'
            except:
                print u'delete fail'

    def update(self,tableName,updateRow,selectRow):
        sql = 'update '+tableName+' set '
        for key in updateRow:
            sql += key + '=' + ('%s' if type(updateRow[key]) == int else '"%s"')%updateRow[key] + ' and '
        sql = sql[:-4]
        sql += 'where '
        for key in selectRow:
            sql += key + '=' + ('%s' if type(selectRow[key]) == int else '"%s"')%selectRow[key] + ' and '
        sql = sql[:-4]
        try:   
            self.cursor.execute(sql)
            self.cx.commit()
            self.cursor.close()
            self.cx.close()
            print u'update success'
        except:
            print u'update fail'


if __name__ == '__main__':
    db = db_control()
    # db.insert('huobi',0,0,'KlausQiu','qiu','11111111111111','2222222222222')
    # db.insert('huobi',1,1,'MoonQiu','qiu','12222111111','22333222222')
    c = db.select('huobi')
    print c
    # d1 = {'name':'qiu'}
    # d2 = {'id':1}
    # db.update('huobi',d1,d2)
    # db.delete('huobi',id=1,name='MoonQiu')
    #db.insert('huobi',0,0,'KlausQiu','qiu','11111111111111','2222222222222')
    # db.creatTable('huobi','id integer primary key','uid integer','name varchar(10) UNIQUE','password TEXT','access_key text UNIQUE','secret_key text UNIQUE')
    