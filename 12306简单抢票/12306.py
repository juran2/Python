#!/usr/bin/python
# -*- coding: UTF-8 -*-

from prettytable import PrettyTable
import urllib.request
import datetime
import time
import json
import ssl
import re

def help():
    message = '''
运行环境 win10,x64,python3.5
这是一个12306余票查询的小程序,最终运行train_list = get_train_list()返回相应火车票的相关信息,
再运行print_ticket_info(train_list)将信息打印
所需要的库:
from prettytable import PrettyTable
import urllib.request
import datetime
import time
import json
import ssl
import re
prettytable 使打印出来的信息更美观,如果不想安装该库,直接打印train_lsit即可,train_list中的元素从左往右依次代表
|  车次 | 出发站 | 终点站 | 出发时间 | 到达时间 | 运行时间 | 商务 | 一等座 | 二等座 | 高级软卧 | 软卧 | 动卧 | 硬卧 | 硬座 | 无座 |
'''
    print(message)

ssl._create_default_https_context = ssl._create_unverified_context

def get_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"}
    req = urllib.request.Request(url = url, headers = headers)
    html = urllib.request.urlopen(req).read()
    html = html.decode("utf-8")
    return html

def get_stations():
    try:
        with open('station.json','r') as f:
            dict_station = json.load(f)
    except:
        url_station = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9025"
        stations = get_html(url_station)
        dict_station = {}
        station_list = stations.split('@')
        for station in station_list:
            try:
                s = station.split("|")
                dict_station[s[1]] = s[2]
            except:
                pass
        with open('station.json','w') as f:
            json.dump(dict_station,f)
    return dict_station

def get_start_arrive_station(s):
    while True:
        from_station = input("请输入出发站: ")
        if from_station in s:
            break
        else:
            print('您输入的出发站地点不存在!!!')
            continue

    while True:
        to_station = input("请输入目的站: ")
        if to_station in s:
            break
        else:
            print('您输入的目的站不存在!!!')
            continue
    return from_station,to_station

def get_start_date():
    today = datetime.date.today()
    # year, month, day = today.year, today.month, today.day
    str_today = str(today)
    while True:
        train_date = input("请输入出发日期(如,2017-09-01): ")
        if re.match(r'\d{4}-\d{2}-\d{2}$', train_date):
            t = train_date.split('-')
            if train_date >= str_today and int(t[2]) <= 31:
                break
            else:
                print('您输入的日期不合法!!!')
                continue
        else:
            print('日期输入格式有错误,请按 year-month-day 格式输出!')
            continue
    return train_date

def get_ticket_info(train_date,from_station,to_station,s):
    url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" %(train_date, s[from_station], s[to_station]) 
    ##print(url)
    while True:
        try:
            html = get_html(url)
            content = json.loads(html)
            break
        except:
##            print('网络错误,正在尝试重新发送请求,请耐心等待...')
            time.sleep(3)
            continue
    try:
        train_info = content['data']['result']
    except KeyError:
        print(content['messages'][0])
    return train_info

def extract_ticket_info(train_info,s):
    train_list = []
    for train in train_info:
        t = train.split('|')
        train_id, start_station, arrive_station, start_time, arrive_time, run_time = t[3],t[6],t[7],t[8],t[9],t[10]
        start_station = list(s.keys())[list(s.values()).index(start_station)]
        arrive_station = list(s.keys())[list(s.values()).index(arrive_station)]
        train = [train_id, start_station, arrive_station, start_time, arrive_time, run_time]
        [shangwu, yideng, erdeng, gaojiruanwo, ruanwo, dongwo, yingwo, yingzuo, wuzuo] = t[-4],t[-5],t[-6],t[-15],t[-13],t[-3],t[-8],t[-7],t[-10]
        seat = [shangwu, yideng, erdeng, gaojiruanwo, ruanwo, dongwo, yingwo, yingzuo, wuzuo]
        train.extend(seat)
        train_list.append(train)
    return train_list

def print_ticket_info(train_list):
    x = PrettyTable(["train_id","start_station","arrive_station","start_time","arrive_time","run_time","shangwu","yideng","erdeng","gaojirw","ruanwo","dongwo","yingwo","yingzuo","wuzuo"])
    x.padding_width = 1
    for train in train_list:
        x.add_row(train)
    print(x)


# 获取车站名和相应代号对照字典,如 {北京:BJP,...}
# 获取方式有两种:从本地(当前目录下)加载之前已经存入的表中获取,若文件不存在,则从网站中获取(在网络不佳的情况下比较耗时间)
s = get_stations()
# 根据输入的车站得到其代号
from_station,to_station = get_start_arrive_station(s)
# 获取用户输入的出发日期
train_date = get_start_date()

def get_train_list():    
    # 根据起始站,火车出发时间向网站发起请求获取车次信息
    train_info = get_ticket_info(train_date,from_station,to_station,s)
    # 提取车次信息
    train_list = extract_ticket_info(train_info,s)
    return train_list

def get_specific_ticket(row,column):
    train_list = get_train_list()
    train_specific = train_list[row]
    print(train_specific[:6],train_specific[column],'正在抢票...')
    return train_specific[column]

def snatch_ticket(row,colume,char):
    while True:
        ticket1 = get_specific_ticket(row,colume)
        if ticket1 != char:
            print('ticket1,票价有变化')
            break
        else:
            time.sleep(30)

if __name__ == "__main__":
    #  获取所需列车信息列表
    train_list = get_train_list()
    # 打印车次信息
    print_ticket_info(train_list)
    
    #  获取所需列车信息列表
    train_list = get_train_list()
    # 打印车次信息
    print_ticket_info(train_list)