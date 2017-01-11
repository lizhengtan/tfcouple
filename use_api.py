#coding=utf8
import json
import sys
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree  as ET

reload(sys)
sys.setdefaultencoding('utf8')

def ip2add(ip):
    url = 'http://apis.juhe.cn/ip/ip2addr?ip=%s&key=8509aa18012d75a830387423e935e6fe&dtype=json' % ip
    data = requests.get(url)
    json_data = json.loads(data.text)
    json_result = json_data['result']
    json_area = json_result['area']
    json_location = json_result['location']
    #大部分返回的城市不能直接用于查询天气,可以用split用市字分割
    return json_area


def city_weather(city):
    #城市位置转天气，只获取了本日天气
    url = 'http://op.juhe.cn/onebox/weather/query?cityname=%s&key=1532a78a9ffb0bcb3786cf22501dd4be' % city
    data = requests.get(url)
    json_data = json.loads(data.text)
    json_result = json_data['result']
    json_data = json_result['data']
    json_pm = json_data['pm25']
    json_pm = json_pm['pm25']
    json_weather = json_data['weather']
    weather_day = json_weather[0]['info']['day']# 0代表本日天气，1代表明天，以此类推，有一周的天气
    weather_night = json_weather[0]['info']['night']
    temperature = weather_night[2].encode('utf-8') + '℃~' + weather_day[2].encode('utf-8') + '℃'
    if weather_day[1].encode('utf-8') == weather_night[1].encode('utf-8'):
        weather = weather_day[1].encode('utf-8')
    else:
        weather = weather_day[1].encode('utf-8') + '转' + weather_night[1].encode('utf-8')
    if weather_day[4].encode('utf-8') == '微风':
        wind = weather_day[4].encode('utf-8')
    else:
        wind = weather_day[4].encode('utf-8')
    quality = json_pm['quality'].encode('utf-8')
    pm = 'pm:' + json_pm['pm25'].encode('utf-8')
    weather_data=[weather,temperature,wind,pm]
    return weather_data