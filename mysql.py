#coding=utf8
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def select_mysql(sql):
    conn = MySQLdb.connect(host='localhost', user='root',passwd='shiWOlp123',port=3306,db='myweb',charset='utf8' )
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def query_mysql(sql):
    print sql
    conn = MySQLdb.connect(host='localhost', user='root',passwd='shiWOlp123',port=3306,db='myweb',charset='utf8' )
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

