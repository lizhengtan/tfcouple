#coding=utf8
import urllib

from flask import redirect
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from get_local_info import *
from use_api import *
from mysql import *

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

#全局变量
user_name='李政倓'


@app.route('/',methods=['GET', 'POST'])
def index():
    ip = request.remote_addr
    try:
        add = ip2add(ip)
        city = add.split('市')[0]
        city = urllib.quote(str(city))
        weather = city_weather(city)
    except:
        print '未获取到天气信息'
        weather = ''
    return render_template('index.html',weather=weather)

@app.route('/login',methods=['GET','POST'])
def login():
    data = json.loads(request.data)
    user = data['user']
    psw = data['psw']

@app.route('/register',methods=['GET','POST'])
def register():
    ip = request.remote_addr
    try:
        add = ip2add(ip)
        city = add.split('市')[0]
        city = urllib.quote(str(city))
        weather = city_weather(city)
    except:
        print '未获取到天气信息'
        weather = ''
    #data = json.loads(request.data)
    #user = data['user']
    #psw = data['psw']
    #email = data['email']
    return render_template('register.html',weather=weather)

@app.route('/search_user',methods=['GET','POST'])
def search_user():
    data = json.loads(request.data)
    user = data['user']
    sql = 'select * from user where user=\'%s\'' % user
    result = select_mysql(sql)
    if len(result) == 0:
        print '未注册'
        return jsonify({'ok': True})
    else:
        print '已注册'
        return jsonify({'ok': False})

@app.route('/insert_user',methods=['GET','POST'])
def insert_user():
    data = json.loads(request.data)
    user = data['user']
    psw = data['psw']
    email = data['email']
    sql = 'insert into user (user,psw,email) values (\'%s\',\'%s\',\'%s\')' % (user,psw,email)
    query_mysql(sql)
    return jsonify({'ok': True})


@app.route('/information',methods=['GET', 'POST'])
def information():
    ip = request.remote_addr
    try:
        add = ip2add(ip)
        city = add.split('市')[0]
        city = urllib.quote(str(city))
        weather = city_weather(city)
    except:
        print '未获取到天气信息'
        weather=''
    information = get_information()
    educations = get_educations()
    works = get_works()
    programs = get_programs()
    skills = get_skills()

    return render_template('information.html',weather=weather,information=information,educations=educations,works=works,programs=programs,skills=skills)

@app.route('/update_information',methods=['GET', 'POST'])
def update_information():
    insertLimit = json.loads(request.data)
    tel = insertLimit['tel']
    email = insertLimit['email']
    update_sql='update resume_information set valid=\'0\''
    query_mysql(update_sql)
    insert_sql='insert into resume_information (name,tel,email) values (\'%s\',\'%s\',\'%s\')' % (user_name,tel,email)
    query_mysql(insert_sql)
    return jsonify({'ok': True})

@app.route('/update_education',methods=['GET', 'POST'])
def update_education():
    insertLimit = json.loads(request.data)
    id = insertLimit['id']
    start = insertLimit['start']
    end = insertLimit['end']
    school = insertLimit['school']
    major = insertLimit['major']
    update_sql='update resume_education set valid=\'0\' where id=\'%s\'' % id
    query_mysql(update_sql)
    insert_sql='insert into resume_education (start,end,school,major) values (\'%s\',\'%s\',\'%s\',\'%s\')' % (start,end,school,major)
    query_mysql(insert_sql)
    return jsonify({'ok': True})

@app.route('/del_education',methods=['GET', 'POST'])
def del_education():
    delLimit = json.loads(request.data)
    id = delLimit['id']
    #含义删除,保留过去操作痕迹,故,仅将有效值置为0
    delete_sql='update resume_education set valid=\'0\' where id=\'%s\'' % id
    query_mysql(delete_sql)
    return jsonify({'ok': True})

@app.route('/insert_education',methods=['GET', 'POST'])
def insert_education():
    insertLimit = json.loads(request.data)
    start = insertLimit['start']
    end = insertLimit['end']
    school = insertLimit['school']
    major = insertLimit['major']
    insert_sql='insert into resume_education (start,end,school,major) values (\'%s\',\'%s\',\'%s\',\'%s\')' % (start,end,school,major)
    query_mysql(insert_sql)
    return jsonify({'ok': True})

@app.route('/update_work',methods=['GET', 'POST'])
def update_work():
    insertLimit = json.loads(request.data)
    id = insertLimit['id']
    start = insertLimit['start']
    end = insertLimit['end']
    place = insertLimit['place']
    job = insertLimit['job']
    describe_1 = insertLimit['describe_1']
    describe_2 = insertLimit['describe_2']
    describe_3 = insertLimit['describe_3']
    update_sql='update resume_work set valid=\'0\' where id=\'%s\'' % id
    query_mysql(update_sql)
    insert_sql='insert into resume_work (start,end,place,job,describe_1,describe_2,describe_3) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (start,end,place,job,describe_1,describe_2,describe_3)
    query_mysql(insert_sql)
    return jsonify({'ok': True})


@app.route('/del_work',methods=['GET', 'POST'])
def del_work():
    delLimit = json.loads(request.data)
    id = delLimit['id']
    #含义删除,保留过去操作痕迹,故,仅将有效值置为0
    delete_sql='update resume_work set valid=\'0\' where id=\'%s\'' % id
    query_mysql(delete_sql)
    return jsonify({'ok': True})

@app.route('/insert_work',methods=['GET', 'POST'])
def insert_work():
    insertLimit = json.loads(request.data)
    start = insertLimit['start']
    end = insertLimit['end']
    place = insertLimit['place']
    job = insertLimit['job']
    describe_1 = insertLimit['describe_1']
    describe_2 = insertLimit['describe_2']
    describe_3 = insertLimit['describe_3']
    insert_sql='insert into resume_work (start,end,place,job,describe_1,describe_2,describe_3) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (start,end,place,job,describe_1,describe_2,describe_3)
    query_mysql(insert_sql)
    return jsonify({'ok': True})

@app.route('/update_program',methods=['GET', 'POST'])
def update_program():
    insertLimit = json.loads(request.data)
    id = insertLimit['id']
    start = insertLimit['start']
    end = insertLimit['end']
    place = insertLimit['place']
    job = insertLimit['job']
    describe_1 = insertLimit['describe_1']
    describe_2 = insertLimit['describe_2']
    describe_3 = insertLimit['describe_3']
    update_sql='update resume_program set valid=\'0\' where id=\'%s\'' % id
    query_mysql(update_sql)
    insert_sql='insert into resume_program (start,end,name,job,describe_1,describe_2,describe_3) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (start,end,place,job,describe_1,describe_2,describe_3)
    query_mysql(insert_sql)
    return jsonify({'ok': True})


@app.route('/del_program',methods=['GET', 'POST'])
def del_program():
    delLimit = json.loads(request.data)
    id = delLimit['id']
    #含义删除,保留过去操作痕迹,故,仅将有效值置为0
    delete_sql='update resume_program set valid=\'0\' where id=\'%s\'' % id
    query_mysql(delete_sql)
    return jsonify({'ok': True})

@app.route('/insert_program',methods=['GET', 'POST'])
def insert_program():
    insertLimit = json.loads(request.data)
    start = insertLimit['start']
    end = insertLimit['end']
    place = insertLimit['place']
    job = insertLimit['job']
    describe_1 = insertLimit['describe_1']
    describe_2 = insertLimit['describe_2']
    describe_3 = insertLimit['describe_3']
    insert_sql='insert into resume_program (start,end,name,job,describe_1,describe_2,describe_3) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (start,end,place,job,describe_1,describe_2,describe_3)
    query_mysql(insert_sql)
    return jsonify({'ok': True})

@app.route('/update_skill',methods=['GET', 'POST'])
def update_skill():
    insertLimit = json.loads(request.data)
    id = insertLimit['id']
    describe = insertLimit['describe']
    update_sql='update resume_skill set valid=\'0\' where id=\'%s\'' % id
    query_mysql(update_sql)
    insert_sql='insert into resume_skill (skill) values (\'%s\')' % (describe)
    query_mysql(insert_sql)
    return jsonify({'ok': True})

@app.route('/del_skill',methods=['GET', 'POST'])
def del_skill():
    delLimit = json.loads(request.data)
    id = delLimit['id']
    #含义删除,保留过去操作痕迹,故,仅将有效值置为0
    delete_sql='update resume_skill set valid=\'0\' where id=\'%s\'' % id
    query_mysql(delete_sql)
    return jsonify({'ok': True})

@app.route('/insert_skill',methods=['GET', 'POST'])
def insert_skill():
    insertLimit = json.loads(request.data)
    describe = insertLimit['describe']
    insert_sql='insert into resume_skill (skill) values (\'%s\')' % (describe)
    query_mysql(insert_sql)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True)
