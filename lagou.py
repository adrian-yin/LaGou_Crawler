#!/usr/bin/python3
##########################################################################
# File Name: lagou.py
# Author: Adrian
# mail: adrianyin@yeah.net
# Created Time(UTC): 2019年07月27日 星期六 15时51分09秒
# 按输入爬取拉勾网数据，保存到mysql数据库中
#########################################################################

import requests
import time
import random
import pymysql.cursors


def connect_mysql():
    # 连接mysql数据库
    
    global keyword

    user = input("请输入数据库user：")
    password = input("请输入数据password：")
    connect = pymysql.connect(
            host = "localhost",
            user = user,
            password = password,
            db = "lagou",
            charset = "utf8mb4",
            cursorclass = pymysql.cursors.DictCursor,
            # 创建关键词相应table
            init_command = ('CREATE TABLE {} ('
                'id int auto_increment primary key not null,'
                'companyShortName varchar(50),'
                'companyFullName varchar(100),'
                'positionName varchar(100),'
                'jobNature varchar(10),'
                'salary varchar(20),'
                'education varchar(10),'
                'workYear varchar(10),'
                'city varchar(10),'
                'linestation varchar(300),'
                'financeStage varchar(20),'
                'companySize varchar(20))').format(keyword.replace("+", "p").replace("#", "SHARP").replace(".", "dot"))
            ) 

    return connect


def insert_mysql(connect, info):
    # 数据写入数据库

    global keyword

    with connect.cursor() as cursor:
        sql = "INSERT INTO {} (companyShortName, companyFullName, positionName, jobNature, salary, education, workYear, city, linestation, financeStage, companySize) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')".format(keyword.replace("+", "p").replace("#", "SHARP").replace(".", "dot"))
        cursor.execute(sql%info)
    connect.commit()


def get_data(url, page):
    
    global keyword

    # 构建post数据，pn页码，kd查询管检测
    data = {"first": "true", "pn": page, "kd": keyword}

    # 拉勾网反爬虫机制很严格，请求头要尽量完善
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
	"Host": "www.lagou.com",
	"Referer": "https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput=".format(keyword),
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    }

    # 建立session向主地址发送get请求获取cookie
    s = requests.Session()
    main_url = "https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput=".format(keyword)
    s.get(main_url, headers = headers)
    cookie = s.cookies
    
    # 发送post请求获取json字典
    data_dict = requests.post(url, data, headers = headers, cookies = cookie).json()
    
    # 通过字典获取信息
    info_list = []
    for i in data_dict["content"]["positionResult"]["result"]:
        info = []
        info.append(i.get("companyShortName", "无"))
        info.append(i.get("companyFullName", "无"))
        info.append(i.get("positionName", "无"))
        info.append(i.get("jobNature", "无"))
        info.append(i.get("salary", "无"))
        info.append(i.get("education", "无"))
        info.append(i.get("workYear", "无"))
        info.append(i.get("city", "无"))
        info.append(i.get("linestaion", "无"))
        info.append(i.get("financeStage", "无"))
        info.append(i.get("companySize", "无"))
        info_list.append(info)

    return info_list


def main():

    url = "https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false"
    # keyword全局多次使用，设为全局变量
    global keyword
    keyword = input("请输入要爬取的关键词：")
    
    connect = connect_mysql()
    
    for page in range(1, 31):
        print("正在爬取第{}页...".format(page))
        info_list = get_data(url, page)
        for info in info_list:
            insert_mysql(connect, tuple(info))
        
        # 避免被反爬虫识破，每10-19秒发送一次请求
        time.sleep(random.randint(10, 20))

    # 数据库连接要关闭
    connect.close()

if __name__ == "__main__":
    main()
