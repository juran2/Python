#!/usr/bin/python
# -*- coding: UTF-8 -*-

########脚本概括########
#1、下载Laravel官网所有的教程，包括各个版本
#2、主要通过‘article-link-1’关键字段来遍历每一篇教程
#3、下载等待时间根据网速进行更改

########不足之处########
#1、没有实现下载路径的选择，下载路径为默认
#2、没有实现等待上一个保存完后再保存下一个，而是估计时间跳转到下一个

########运行环境-知识点########
#1、python + chromedriver + selenium + pywin32
#2、模拟键盘鼠标操作，实现网页自动化

# @ made by JuRan

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep
import win32api
import win32con

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')
option.add_argument('--start-maximized')  #窗口最大化
browser = webdriver.Chrome(chrome_options=option)

class SaveLara(object):    #定义一个类来保存离线网页，同理于chrome浏览器直接ctrl+s保存
    def __init__(self,url,pages,versions,title):    #初始化类，分别为入口网址、laravel版本、教程页数和教程标题
        self.url=url
        self.ver=versions
        self.pages=pages
        self.title=title

    def ergodic(self): 
        print('==========================') 
        #进入初始化网页
        browser.get(self.url)
        print('《'+self.title+'》'+'已打开...')
        browser.refresh()
        print('刷新获得最新页面...')
        sleep(2) 

        print('==========================') 
        print('开始遍历...') 
        ###########遍历各个版本
        #模拟按键找到版本选择，然后tab切换对应次数，回车确定刷新网页
        for version_num in range(1,self.ver+1):
            version=browser.find_element_by_css_selector('.ui.right.floated.buttons')
            ActionChains(browser).click(version).perform()
            for times in range(0,version_num):
                win32api.keybd_event(9, 0, 0, 0)           # 按下tab
                win32api.keybd_event(9,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
            win32api.keybd_event(13, 0, 0, 0)           # 按下enter
            win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
            sleep(2)   #等待加载网页

            ###########遍历每一篇教程
            #找到对应网页，模拟点击，然后模拟ctrl+s，保存为离线网页
            for i in range(1,self.pages+1):
                article=browser.find_element_by_id('article-link-'+str(i))
                ActionChains(browser).click(article).perform()
                print('正在下载网页：'+ browser.find_element_by_id('article-link-'+str(i)).text)
                sleep(2)   #等待网页加载
                win32api.keybd_event(17, 0, 0, 0)           # 按下ctrl
                win32api.keybd_event(83, 0, 0, 0)           # 按下s
                win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
                win32api.keybd_event(83,0,win32con.KEYEVENTF_KEYUP,0)
                sleep(1)
                win32api.keybd_event(13, 0, 0, 0)           # 按下enter
                win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
                sleep(1)
                
                sleep(10)   #等待下载网页的时间，根据网速来设置
   
        
        
def login(main_page):
    #因为课程是收费的，所以需要购买了课程的账号登陆，才能下载完成的教程
    browser.get(main_page)
    browser.refresh()
    sleep(2) 
    #点击登陆按钮
    login=browser.find_element_by_css_selector('.mr-4.no-pjax.login_required')
    ActionChains(browser).click(login).perform()
    sleep(2)   
    #输入账号密码
    print('==========================') 
    print('登陆账号') 
    browser.find_element_by_name('username').send_keys('965569983@qq.com')
    browser.find_element_by_name('password').send_keys('juran1993')
    browser.find_element_by_name('password').send_keys(Keys.ENTER)



if __name__ == '__main__':

    main_page='https://learnku.com/laravel/courses'                                      #登陆页面
    l01='https://learnku.com/courses/laravel-essential-training/5.8/about-the-book/4046' #web开发实战入门
    l02='https://learnku.com/courses/laravel-intermediate-training/5.8/preface/4125'     #web开发实战进阶 
    l03='https://learnku.com/courses/laravel-advance-training/5.8/preface/3976'          #实战构架API服务器
    l04='https://learnku.com/courses/laravel-weapp/5.5/preface/1421'                     #微信小程序从零到发布
    l05='https://learnku.com/courses/laravel-shop/5.8/preface/4206'                      #电商实战
    l06='https://learnku.com/courses/ecommerce-advance/5.8/preface/4234'                 #电商进阶

    courses=[l01,l02,l03,l04,l05,l06]  #课程列表
    pages=[79,81,70,56,76,83]          #页面列表
    versions=[4,3,3,1,3,3]             #laravel版本列表
    titles=['web开发实战入门','web开发实战进阶','实战构架API服务器','微信小程序从零到发布','电商实战','电商实战']

    print('脚本开始运行...')
    print('进入主页，开始登陆...')
    login(main_page)        #登陆账号

    #通过调用SaveLara类的ergodic方法，来遍历每一门课程
    for i in range(0,len(courses)+1):
        SaveLara(courses[i],pages[i],versions[i],titles[i]).ergodic()

    print('======================')
    print('全部下载完成！')
    browser.close()
    print('关闭浏览器!')