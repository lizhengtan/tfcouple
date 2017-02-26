#coding:utf-8
import sys
sys.path.append('../')
from mysql import *
import requests
from bs4 import BeautifulSoup
import time
import urllib2

xici_headers = {
	'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWYzMTkxNzNjYzY1MjA1YzAzMzdhNmE0ODVjYzllNTExBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMThReVZXWEx0RE9JZ3BhYk9oWHlFMVZEditXeVptTmtaejgrMG5ZYzdSUk09BjsARg%3D%3D--1f0731110dab415404d0c19ab3794ade88369bd3; CNZZDATA1256960793=301945704-1487384554-http%253A%252F%252Fwww.baidu.com%252F%7C1487384554',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'If-None-Match':'W/"a6dfdca5041df77bb7055cff6d0490e4"',
	'Host':'www.xicidaili.com',
	'Upgrade-Insecure-Requests':'1',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

kuai_headers = {
	'Cookie':'_gat=1; channelid=0; sid=1487395131493568; _ga=GA1.2.198410209.1486659361; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1486659361; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1487395604',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	'Host':'www.kuaidaili.com',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
def get_xici_ip(page_num):
	url = 'http://www.xicidaili.com/nn/%s' % page_num
	data = requests.get(url,headers = xici_headers)
	soup = BeautifulSoup(data.text,'lxml')
	table_database = soup.select('tr')
	for table_data in table_database:
		database = table_data.select('td')
		try:
			ip = database[1].get_text().strip()
			port = database[2].get_text().strip()
			ipport = ip + ':' + port
			sql = 'insert into ip_list values (\'%s\',\'%s\',\'%s\')' % (ip,port,ipport)
			query_mysql(sql)
		except:
			pass


def get_kuaidaili_ip(page_num):
	url = 'http://www.kuaidaili.com/free/inha/%s/' % page_num
	data = requests.get(url,headers = kuai_headers)
	soup = BeautifulSoup(data.text,'lxml')
	table_database = soup.select('tr')
	for table_data in table_database:
		database = table_data.select('td')
		try:
			ip = database[0].get_text().strip()
			port = database[1].get_text().strip()
			ipport = ip + ':' + port
			sql = 'insert into ip_list values (\'%s\',\'%s\',\'%s\')' % (ip,port,ipport)
			query_mysql(sql)
		except:
			pass

def check_ip(ipport):
	proxy = {'http':ipport}
	#print proxy
	test_url = "http://www.baidu.com"
	#timeout 设置为10，如果你不能忍受你的代理延时超过10，就修改timeout的数字
	proxy = urllib2.ProxyHandler(proxy)
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	try:
		response = urllib2.urlopen(test_url,timeout = 1)
		print response.code
		sql = 'insert into ture_ip values (\'%s\')' % ipport
		query_mysql(sql)
	except:
		sql = 'delete from ip where ipport=\'%s\'' % ipport
		query_mysql(sql)
		sql = 'insert into ip_list (ipport) values (\'%s\')' % ipport
		query_mysql(sql)
	

sql_str = 'select ipport from ip'
databases = select_mysql(sql_str)
for database in databases:
	for data in database:
		check_ip(data)


