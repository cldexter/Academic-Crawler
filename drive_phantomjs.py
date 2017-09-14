# -*- coding: utf-8 -*-
# !/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from BeautifulSoup import BeautifulSoup

headers = {'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Referer':"https://www.baidu.com", 
"Connection": "keep-alive",
"Pragma": "max-age=0",
"Cache-Control": "no-cache",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding": "gzip, deflate, sdch",
"Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.6"
}

def open_phantomjs(url):
    time_out = 30
    try_time = 3

    dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = (headers)#header未来可以写成一个大集合，随机的
    dcap["phantomjs.page.settings.loadImages"] = False#不载入图片，以加快速度
    
    obj = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap) #加载网址
    obj.set_page_load_timeout(time_out)#设定网页加载超时
    obj.set_window_size('1024','1280') 
    i = 0
    for i in range(try_time):
        try:
            obj.get(url)#打开网址
            obj.find_element_by_link_text("Next >").click()
            print "second page"
            soup = BeautifulSoup(obj.page_source)
            content = soup.findAll(name="div",attrs={"class":"rslt"})#把sc_content类的抓过来

            print len(content)
            obj.save_screenshot("1.png")   #截图保存
            obj.find_element_by_link_text("Next >").click()
            print "third page"
            obj.save_screenshot("2.png")   #截图保存
            break
        except Exception as e:
            print "Retry " + str(i) + " time"
            print e
            i = i + 1
    if i == try_time:
        print "Cannot connect to the server"
    obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能

open_phantomjs('https://www.ncbi.nlm.nih.gov/pubmed/?term=dexter+chen')