#coding:utf-8
import requests
from bs4 import BeautifulSoup
import MySQLdb
import sys
import urllib2
import time
import random
from mysql import *


reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
	'Cookie':'lianjia_uuid=f6677545-c12a-46c8-b370-5a9655be566a; _jzqy=1.1486389663.1486389663.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _jzqckmp=1; lianjia_token=2.000b8697427293bca11a2bbe73a9bd3f6b; gr_user_id=caeb4c54-0bef-4e4d-8456-584bdbac8e88; cityCode=su; ubt_load_interval_b=1486391030928; ubta=1641808036.1545063108.1486390988823.1486391030340.1486391030983.7; ubtc=1641808036.1545063108.1486391030988.87761F728996BDC0FF655A96953E1205; ubtd=7; logger_session=6b66878141861dd9b2a57af36c732932; select_city=110000; _jzqx=1.1486394555.1486394555.1.jzqsr=bj%2Elianjia%2Ecom|jzqct=/chengjiao/dongcheng/hy1/.-; ljref=pc_sem_baidu_ppzq_x; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _smt_uid=5898819f.42db917a; _jzqa=1.2500562980422840000.1486389663.1486389663.1486394555.2; _jzqc=1; _jzqb=1.23.10.1486394555.1; _ga=GA1.2.1836998501.1486389665; lianjia_ssid=4f6e1518-ec9c-4892-9f9b-e67353e8d86d',
}


city_path = ['heping','nankai','hexi','hebei','hedong','hongqiao','xiqing','beichen','dongli','jinnan','tanggu','kaifaqu']

def get_data(city,url,num):
	url = url + 'pg' + str(num)
	print url
	req = urllib2.Request(url,headers=headers) 
	response = urllib2.urlopen(req)
	#data = requests.get(url , headers = headers)
	#用reuqests会乱码，原因暂时不清楚
	time.sleep(random.randint(1,90))
	soup = BeautifulSoup(response,'lxml')
	#titles = soup.find_all("div",class_="title")
	dates = soup.find_all("div",class_="dealDate")
	prices = soup.find_all("div",class_="totalPrice")
	average_prices = soup.find_all("div",class_="unitPrice")
	urlss = soup.select('body > div > div > ul > li > div > div.title > a')
	for date,price,average_price,urls in zip(dates,prices,average_prices,urlss):
		print date.get_text(),price.get_text(),average_price.get_text(),urls.get('href')
		sql_str = 'insert into lianjia_tianjin values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (city,date.get_text(),price.get_text(),average_price.get_text(),urls.get('href'))
		try:
			query_mysql(sql_str)
		except:
			pass
	del urlss

def check_condition(city,xiaoqu):
	url = 'http://tj.lianjia.com/chengjiao/rs%s' % xiaoqu
	req = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(req)
	time.sleep(random.randint(1,90))
	soup = BeautifulSoup(response,'lxml')
	sum_nums = soup.select('body > div.content > div.leftContent > div.resultDes.clear > div.total.fl > span')

	dates = soup.find_all("div",class_="dealDate")
	prices = soup.find_all("div",class_="totalPrice")
	average_prices = soup.find_all("div",class_="unitPrice")
	urlss = soup.select('body > div > div > ul > li > div > div.title > a')
	for date,price,average_price,urls in zip(dates,prices,average_prices,urlss):
		print date.get_text(),price.get_text(),average_price.get_text(),urls.get('href')
		sql_str = 'insert into lianjia_tianjin values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (city,date.get_text(),price.get_text(),average_price.get_text(),urls.get('href'))
		try:
			query_mysql(sql_str)
		except:
			pass
	del urlss

	for sum_num in sum_nums:
		if 0 < int(sum_num.get_text()) < 3500:
			print url + '|||' + sum_num.get_text()
			page_num = int(sum_num.get_text()) / 30 + 1
			for num in range(1,page_num):
				get_data(city,url,num)
			return 'ture'
 


sql_str = 'select title,district from lianjia_tianjin_list order by title desc '
database = select_mysql(sql_str)
for data in database:
	check_condition(data[1],data[0])

