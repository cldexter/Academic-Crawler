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
sum_page_number = 3
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

# def generate_record(self): # 从抓取的原始素材产生记录
#     m = 0
#     n = 0
#     title_start_with = "linksrc=docsum_title\">"#标记查找标题开头
#     title_end_with = "</a>"#查找标题的结尾
#     journal_start_with = 'title='#查找期刊开头
#     journal_end_with = '\">'#查找期刊结尾
#     for m in range(len(content)):  # 有多少重复多少
#         author[m] = str(author[m])[16:-4]  # 作者
#         journal_end = str(journal[m]).find(journal_end_with)
#         journal[m] = str(journal[m])[26:journal_end].replace('<b>', '').replace('</b>', '')  # 期刊
#         pmid[m] = str(pmid[m])[4:-5]  # pmid
#         title_start = str(title[m]).find(title_start_with) + 22
#         title[m] = str(title[m])[title_start:-8].replace('<b>', '').replace('</b>', '')  # 论文名
#         issue[m] = re.search("[1-2][09][0-9]{2}", str(issue[m])).group(0)  # 刊号
#         if not(check_pmid(pmid[m])): # 如果之前没有这篇文章
#             abstract = crawl_abstract_page(pmid[m]) # 获取abstract
#             if abstract: # 如果能够返回正确的abstract，记录；否则留给下一次抓取（不记录，视作新论文）
#             record = author[m],issue[m],pmid[m],title[m],journal[m],abstract[0],abstract[1] #这里的abstract[0]是这篇文章的abstract,abstract[1]是全文下载的链接合集
#             data_write(record,project_name,"data") # 录入数据文件
#             pmid_write(pmid[m],project_name,"history") # 录入历史文件
#             n += 1  # 记录多少篇新文章
#             print u"  New: " + str(title[m])  # 录入
#             time.sleep(5)
#         else:
#             print u" ○ Skipped NO." + str(m+1) + u": Already retrieved"
#     print u"  Retrieved " + str(n) + u" new articles"

time_out = 10
tries_1 = 2
tries_2 = 3
dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
dcap["phantomjs.page.settings.userAgent"] = (headers)  # header未来可以写成一个大集合，随机的
dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
obj = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器
obj.set_page_load_timeout(time_out)  # 设定网页加载超时,超过了就不加载
# obj.set_window_size('1024', '1280')  # 设定虚拟浏览器窗口大小
while(tries_1 > 0):
    try:
        obj.get(url)
        soup = BeautifulSoup(obj.page_source)
        doc = soup.findAll(name="div", attrs={"class": "rslt"})
        content.append(doc)
        
        print "first sum-page"
        print len(content)
        obj.save_screenshot('page1.png')
        break
    except Exception as e:
        print e
        print "Retrying loading first sum page"
        tries_1 -= 1

if tries_1 == 0:
    print "fail to read the first sum page"

if len(content) != 0:
    while(sum_page_number >0):
        while(tries_2 >0):
            try:
                obj.find_element_by_link_text("Next >").click() #直接就点开“下一页”，从第二页开始
                soup = BeautifulSoup(obj.page_source)
                doc = soup.findAll(name="div", attrs={"class": "rslt"})
                content.append(doc)
                obj.save_screenshot('page'+str(3-sum_page_number)+'.png')
                sum_page_number -= 1
                break
            except Exception as e:
                print e
                print "Retrying loading " + str(sum_page_number) + " page"
                tries_2 -= 1
        if tries_2 == 0:
            break
            print "Could not load page"

obj.quit()

print len(content)
print content
    
    # author = soup.findAll(name='p', attrs={"class": "desc"})  
    # journal = soup.findAll(name="span", attrs={'class': 'jrnl'})  
    # title = soup.findAll(name='p', attrs={"class": "title"})  
    # issue = soup.findAll(name="p", attrs={'class': 'details'}) 
    # pmid = soup.findAll(name="dd") 
    


# while(tries > 0):
#     try:
#         obj.get(url)  # 打开网址
#         while(sum_page_number > 0):
#             obj.find_element_by_link_text("Next >").click() #直接就点开“下一页”，从第二页开始
#             soup = BeautifulSoup(obj.page_source)
#             content.append.str(soup.findAll(name="div", attrs={"class": "rslt"})) 
#             author = soup.findAll(name='p', attrs={"class": "desc"})  
#             journal = soup.findAll(name="span", attrs={'class': 'jrnl'})  
#             title = soup.findAll(name='p', attrs={"class": "title"})  
#             issue = soup.findAll(name="p", attrs={'class': 'details'}) 
#             pmid = soup.findAll(name="dd") 
#             # generate_record() # 直接产生结果   
#         break
#     except Exception as e:
#         print "Retry " + str(i) + " time"
#         print e
#         tries -= 1
# if i == tries:
#     print " Error: Cannot connect to the server"
obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能