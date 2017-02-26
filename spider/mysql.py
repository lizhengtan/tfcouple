#coding=utf8
import MySQLdb
import sys

import time

reload(sys)
sys.setdefaultencoding('utf8')


def select_mysql(sql):
    stime = time.time()
    conn = MySQLdb.connect(host='localhost', user='root',passwd='shiWOlp123',port=3306,db='myweb',charset='utf8' )
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    etime = time.time()
    print 'sql运行时间:%ss' % (etime-stime)
    return data

def query_mysql(sql):
    stime = time.time()
    conn = MySQLdb.connect(host='localhost', user='root',passwd='shiWOlp123',port=3306,db='myweb',charset='utf8' )
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    etime = time.time()
    print 'sql运行时间:%ss' % (etime-stime)

