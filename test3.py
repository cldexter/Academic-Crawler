# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: search_pubmed.py
   Description: search for defined words combination
   Author: Dexter Chen
   Date：2018-08-25
-------------------------------------------------
   # 爬虫蜘蛛的作用：传入关键词与数量 1.计算多少sum page用phantomjs
   # 2.用request爬第一个sum page 3.用phantomjs爬剩下的页面
   # 4.每爬一个页面（不管怎么爬的）都用BS4解析，获取基本信息
   # 5.判断是否为新 6.用request爬取abstract页面，用BS4解析
   # 7.储存论文 8.输出json
-------------------------------------------------
   Change Log:
   2018-08-26: 重写所有蜘蛛，使用面相对象的办法
-------------------------------------------------
"""
import time
import sys
import math
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from BeautifulSoup import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

reload(sys)
sys.setdefaultencoding('utf8')

# header不要轻易该，反复测试后选择的
headers = {'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Referer': "https://www.ncbi.nlm.nih.gov/pubmed",
           "Connection": "keep-alive",
           "Pragma": "max-age=0",
           "Cache-Control": "no-cache",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, sdch",
           "Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.6"
           }

key_words = "lactobacillus,johnsonii"  # 输入关键词，关键词是一个集合
record_number = 60  # 需要爬多少个
project_name = "lactobacillus"  # 项目的名字

# 实例内部设定
# sum_page_number = math.ceil(record_number / 20)  # 每页20个，计算共多少页
sum_page_number = 4 # sum-page总数，用phantomjs爬的，是这个数-1
url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + key_words.replace(",", "+") # 最初的查询网址

# 实例内部容器
content = [] # 把sc_content类的抓过来；每次抓取新页面都清空
author = [] # author合集；每次抓取新页面都清空
journal = [] # 期刊合集；每次抓取新页面都清空
title = [] # 名字与连接的合集；每次抓取新页面都清空
issue = [] # 年份的合集；每次抓取新页面都清空
pmid = [] # Pmid的合集；每次抓取新页面都清空

abstract_page_url = []  # abstract 链接的合集；每次抓取新页面都清空

output_msg = []  # 用于输出的信息json

record = [] # 用于数据临时存储； 不清空，可无限添加

time_out = 15 # 页面加载时间，预定15秒
tries_first_sum_page = 2 # 尝试获取第一个页面的次数
tries_other_sum_page = 3 # 尝试获取其它每个页面的次数
dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
dcap["phantomjs.page.settings.userAgent"] = (headers)  # header未来可以写成一个大集合，随机的
dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
obj = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器
obj.set_page_load_timeout(time_out)  # 设定网页加载超时,超过了就不加载
# obj.set_window_size('1024', '1280')  # 设定虚拟浏览器窗口大小
while (tries_first_sum_page > 0):
    try:
        obj.get(url)
        # WebDriverWait(obj, 10).until(EC.presence_of_element_located((By.ID, "NCBIFooter_dynamic")))
        break
    except Exception as e:
        # print e
        print "Retrying loading first sum page"
        tries_first_sum_page -= 1

if tries_first_sum_page == 0:
    print "fail to read the first sum page"

while(sum_page_number > 1):#确认需要第二页，如果sum-page只有1页，那就不用再打开
    while(tries_other_sum_page > 0):#尝试多少次，默认尝试3次，不行就打不开
        try:
            obj.implicitly_wait(5)
            obj.find_element_by_link_text("Next >").click() #直接就点开“下一页”，从第二页开始
            # time.sleep(2)
            print "start reading the other page"
            soup = BeautifulSoup(obj.page_source)
            doc = soup.findAll(name="div", attrs={"class": "rslt"})
            content.append(doc)
            obj.save_screenshot('page'+str(4-sum_page_number)+'.png')
            sum_page_number -= 1
            break
        except Exception as e:
            print e
            print "Retrying loading " + str(4-sum_page_number) + " page"
            time.sleep(5)
            tries_other_sum_page -= 1
        # finally:
        #     obj.quit()
    if tries_other_sum_page == 0:
        break
        print "Could not load page"
obj.quit() # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能

print len(content)