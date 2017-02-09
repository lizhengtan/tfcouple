#coding=utf8
from mysql import *
import sys

reload(sys)
sys.setdefaultencoding('utf8')



def get_information():
    sql_str = 'select name,tel,email from resume_information where valid=\'1\''
    databases = select_mysql(sql_str)
    information = {}
    information['name'] = databases[0][0]
    information['tel'] = databases[0][1]
    information['email'] = databases[0][2]
    del databases,sql_str
    return information


def get_educations():
    sql_str = 'select id,start,end,school,major from resume_education where valid=\'1\' order by start desc '
    databases = select_mysql(sql_str)
    educations = []
    for database in databases:
        educations.append(database)
    del databases,sql_str,database
    return educations


def get_works():
    sql_str = 'select id,start,end,place,job,describe_1,describe_2,describe_3 from resume_work where valid=\'1\' order by start desc '
    databases = select_mysql(sql_str)
    works = []
    for database in databases:
        works.append(database)
    del databases,sql_str,database
    return works


def get_programs():
    sql_str = 'select id,start,end,name,job,describe_1,describe_2,describe_3 from resume_program where valid=\'1\' order by start desc'
    databases = select_mysql(sql_str)
    programs = []
    for database in databases:
        programs.append(database)
    del databases,sql_str,database
    return programs


def get_skills():
    sql_str = 'select * from resume_skill where valid=\'1\''
    databases = select_mysql(sql_str)
    skills = []
    for database in databases:
        skills.append(database)
    del databases,sql_str,database
    return skills