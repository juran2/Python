#!/usr/bin/python
# -*- coding: UTF-8 -*-

from splinter.browser import Browser
# from selenium import webdriver
from time import sleep
import traceback

print('haha')

class Buy_Tickets(object):
    #锟斤拷锟斤拷实锟斤拷锟斤拷锟斤拷
    def __init__(self,username,passwd,oder,passengers,dtime,starts,ends):
        self.username =username
        self.passwd = passwd
        #锟斤拷锟轿ｏ拷0锟斤拷锟斤拷锟斤拷锟叫筹拷锟轿ｏ拷一锟轿达拷锟较碉拷锟铰ｏ拷1锟斤拷锟斤拷锟斤拷锟叫筹拷锟轿ｏ拷一锟斤拷锟斤拷锟斤拷
        self.order = order
        #锟剿匡拷锟斤拷
        self.passengers = passengers
        #锟斤拷锟斤拷锟秸碉拷
        self.starts = starts
        self.ends = ends
        #锟斤拷锟斤拷
        self.dtime = dtime
        # self.xb = xb
		# self.pz = pz
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver = Browser(driver_name ="chrome")
        
        #锟斤拷陆锟斤拷锟斤拷实锟斤拷
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name',self.username)
        self.driver.fill('userDTO.password',self.passwd)
        print('请输入验证码...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    def start_buy(self):
        # self.driver.driver.set_window_size(700,500)
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始购票...')
            #加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次查询...' % count)
                    try:
                        self.driver.find_by_text('预订')[self.order-1].click()
                        sleep(2)
                    except Exception as e:
                        print(e)
                        print('预订失败')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        for i in self.driver.find_by_text('预订'):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            print('开始预定')
            sleep(1)
            print('开始选择用户')
            for p in self.passengers:
                self.driver.find_by_text(p).last.click()
                sleep(0.5)
                if p[-1] == ')':
                    self.driver.find_by_id('dialog_xsertcj_ok').click()
            for i in range(10)
                sleep(1)
                print '关闭网页倒计时',10-i
            # print('提交订单')
            # self.driver.find_by_id('submitOrder_id').click()
            # sleep(2)
            # print('确定座位')
            # self.driver.find_by_id('qr_submit_id').click()
            # print('预定成功')
        except Exception as e:
            print(e)
            






if __name__ == '__main__':
    #锟矫伙拷锟斤拷
    username = 'juran1993'
    #锟斤拷锟斤拷
    password = '199303123838'
    #锟斤拷锟斤拷选锟斤拷0锟斤拷锟斤拷锟斤拷锟叫筹拷锟斤拷
    order = 0
    #锟剿匡拷锟斤拷
    passengers = ['鞠然']
    #锟斤拷锟节ｏ拷锟斤拷式为锟斤拷'2018-5-8'
    dtime ='2018-5-10'
    #锟斤拷锟斤拷锟斤拷
    starts = '%u91CD%u5E86%u5317%2CCUW' #重庆北
    #目锟侥碉拷
    ends = '%u9149%u9633%2CAFW' # 酉阳

    # xb = ['硬锟斤拷锟斤拷']
    # pz = ['锟斤拷锟斤拷票']

    # Buy_Tickets(username, password, order, passengers, dtime, starts, ends).start_buy()
    Buy_Tickets(username, password, order, passengers, dtime, starts, ends).start_buy()
