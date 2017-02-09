#coding:utf-8
import requests
from bs4 import BeautifulSoup
import MySQLdb
import sys
import urllib2
import time
import random


reload(sys)
sys.setdefaultencoding('utf-8')


headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
	'Cookie':'lianjia_uuid=f6677545-c12a-46c8-b370-5a9655be566a; _jzqy=1.1486389663.1486389663.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _jzqckmp=1; lianjia_token=2.000b8697427293bca11a2bbe73a9bd3f6b; gr_user_id=caeb4c54-0bef-4e4d-8456-584bdbac8e88; cityCode=su; ubt_load_interval_b=1486391030928; ubta=1641808036.1545063108.1486390988823.1486391030340.1486391030983.7; ubtc=1641808036.1545063108.1486391030988.87761F728996BDC0FF655A96953E1205; ubtd=7; logger_session=6b66878141861dd9b2a57af36c732932; select_city=110000; _jzqx=1.1486394555.1486394555.1.jzqsr=bj%2Elianjia%2Ecom|jzqct=/chengjiao/dongcheng/hy1/.-; ljref=pc_sem_baidu_ppzq_x; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; _smt_uid=5898819f.42db917a; _jzqa=1.2500562980422840000.1486389663.1486389663.1486394555.2; _jzqc=1; _jzqb=1.23.10.1486394555.1; _ga=GA1.2.1836998501.1486389665; lianjia_ssid=4f6e1518-ec9c-4892-9f9b-e67353e8d86d',
}


city_path = ['dongcheng','xicheng','chaoyang','haidian','fengtai','shijingshan','tongzhou','changping','daxing','yizhuangkaifaqu','shunyi','fangshan','mentougou']


def get_data():
	url = 'http://bj.lianjia.com/chengjiao/pg%s' % num
	req = urllib2.Request(url,headers=headers) 
	response = urllib2.urlopen(req)
	#data = requests.get(url , headers = headers)
	#用reuqests会乱码，原因暂时不清楚
	soup = BeautifulSoup(response,'lxml')
	titles = soup.find_all("div",class_="title")
	dates = soup.find_all("div",class_="dealDate")
	prices = soup.find_all("div",class_="totalPrice")
	average_prices = soup.find_all("div",class_="unitPrice")
	urls = soup.select('body > div > div > ul > li > div > div.title > a')
	for title,date,price,average_price,url in zip(titles,dates,prices,average_prices,urls):
		print title.get_text(),date.get_text(),price.get_text(),average_price.get_text(),url.get('href')


valid_list = []
def get_condition(city):#组装筛选条件
	
	for i in range(0,8):
		string = ''
		for j in range(0,8):
			for k in range(0,6):
				if i != 0:
					string += 'p'
					string += str(i)				
				if j != 0:
					string += 'a'
					string += str(j)
				if k != 0:
					string += 'l'
					string += str(k)
				if check_condition(city,string) == 'ture':
					valid_list.append(string)
					print '添加成功'
				string = ''
				break


def check_condition(city,string):
	url = 'http://bj.lianjia.com/chengjiao/' + city + '/' + string
	req = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(req)
	time.sleep(random.randint(1,3))
	soup = BeautifulSoup(response,'lxml')
	sum_nums = soup.select('body > div.content > div.leftContent > div.resultDes.clear > div.total.fl > span')
	for sum_num in sum_nums:
		if int(sum_num.get_text()) < 3500:
			return 'ture'

 
for city in city_path:
	get_condition(city)

for i in valid_list:
	print i
	
print len(valid_list)






