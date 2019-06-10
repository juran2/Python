#!/usr/bin/python
# -*- coding: UTF-8 -*-

#测试版本，下载Laravel开发实战入门的默认最新版本，5.8
#made by JuRan

from splinter.browser import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import win32api
import win32con
import traceback

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
option.add_argument('--start-maximized')  #窗口最大化
browser = webdriver.Chrome(chrome_options=option)

class SaveLava(object):
    def __init__(self,url):
        self.url=url       

    def ergodic(self):  
        print('==========================') 
        print('开始遍历...') 
        for i in range(1,82):
            article=browser.find_element_by_id('article-link-'+str(i))
            ActionChains(browser).click(article).perform()
            print('正在下载网页：article-link-'+str(i))
            sleep(2)   #等待网页加载
            win32api.keybd_event(17, 0, 0, 0)           # 按下ctrl
            win32api.keybd_event(83, 0, 0, 0)           # 按下s
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
            win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
            sleep(1)
            win32api.keybd_event(13, 0, 0, 0)           # 按下enter
            win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
            sleep(1)
            
            sleep(30)   #等待下载网页的时间，根据网速来设置
   
        
        
    def login(self):
        print('==========================') 
        browser.get(self.url)
        print('网页已打开...')
        browser.refresh()
        print('刷新获得最新页面...')
        sleep(2)   
        # #点击登陆按钮
        # login=browser.find_element_by_css_selector('.mr-4.no-pjax.login_required')
        # ActionChains(browser).click(login).perform()
        # sleep(2)   
        # #输入账号密码
        # print('==========================') 
        # print('登陆账号') 
        # browser.find_element_by_name('username').send_keys('965569983@qq.com')
        # browser.find_element_by_name('password').send_keys('juran1993')
        # browser.find_element_by_name('password').send_keys(Keys.ENTER)

        self.ergodic()


if __name__ == '__main__':
    print('脚本开始运行...')
    url='https://learnku.com/courses/laravel-intermediate-training/5.8/preface/4125'
    SaveLava(url).login()