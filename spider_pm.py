# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: search_pubmed.py
   Description: search for defined words combination
   Author: Dexter Chen
   Date：2018-08-25
-------------------------------------------------
   Development Note：
   爬虫蜘蛛的作用：传入关键词与数量 1.计算多少sum page用phantomjs
   2.用request爬第一个sum page 3.用phantomjs爬剩下的页面
   4.每爬一个页面（不管怎么爬的）都用BS4解析，获取基本信息
   5.判断是否为新 6.用request爬取abstract页面，用BS4解析
   7.储存论文 8.输出json
-------------------------------------------------
   Change Log:
   2018-08-26: 重写所有蜘蛛，使用面相对象的办法
   2018-08-29：抓取方法改为采用phantomjs + selenium
-------------------------------------------------
"""
import time
import sys
import math
import json
import requests
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
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

class Spider_pm:  # 爬虫的蜘蛛
    def __init__(self,project_name,key_words,record_number):
        self.key_words = key_words  # 输入关键词，关键词是一个集合
        self.record_number = record_number  # 需要爬多少个
        self.project_name = project_name  # 项目的名字
        # 实例内部设定
        self.sum_page_number = math.ceil(self.record_number / 20)  # 每页20个，计算共多少页
        self.url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + self.key_words.replace(",", "+") # 最初的查询网址
        # 实例内部容器
        self.content = [] # 把sc_content类的抓过来；每次抓取新页面都清空
        self.author = [] # author合集；每次抓取新页面都清空
        self.journal = [] # 期刊合集；每次抓取新页面都清空
        self.title = [] # 名字与连接的合集；每次抓取新页面都清空
        self.issue = [] # 年份的合集；每次抓取新页面都清空
        self.pmid = [] # Pmid的合集；每次抓取新页面都清空
        self.output_msg = []  # 用于输出的信息json

#=====================================================================================
# 以下是需要的小函数
    def cur_file_dir(self):  # 获取脚本路径
        path = sys.path[0]
        return path

    def file_path(self, file_type):  # 用于查询当前的文件位置和名称
        path = self.cur_file_dir() + "/" + self.project_name + "/"
        if file_type == "history":
            return path + self.project_name + "_history.txt"
        if file_type == "data":
            return path + self.project_name + "_data.csv"
        if file_type == "key_words":
            return path + self.project_name + "_key_words.csv"
        else:
            return u" Error: Wrong file type"

    def pmid_read(self, file_type):  # 读取pmid库,自动关闭文件
        with open(self.file_path(file_type), 'r') as f:
            pmid_set = f.read()
        return pmid_set

    def pmid_write(self, pmid, file_type):  # 存入pmid,自动关闭文件
        with open(self.file_path( file_type), "a") as f:
            f.write(pmid + ',')

    def pmid_check(self, pmid):  # pmid在不在历史文件中，在，返回1；如果不在，返回0;用于防止抓多了
        pmid_set = self.pmid_read("history")
        if pmid in pmid_set:
            return 1  # 如果有，说明是旧的
        else:
            return 0  # 如果没有，说明是新的

    def data_read(self, file_type):  # 所有读取都用这个
        data_set = []
        with open(self.file_path(file_type), 'rb') as csvfile:
            data = csv.reader(csvfile, dialect='excel')
            for row in data:
                data_set.append(','.join(row))
        return data_set

    def data_write(self, data, file_type):  # 所有储存都这样弄
        with open(self.file_path(file_type), 'a') as csvfile:
            data_writer = csv.writer(csvfile, dialect='excel')
            data_writer.writerow(data)

    def generate_record(self): # 从抓取的原始素材产生记录
        title_start_with = "linksrc=docsum_title\">"#标记查找标题开头
        title_end_with = "</a>"#查找标题的结尾
        journal_start_with = 'title='#查找期刊开头
        journal_end_with = '\">'#查找期刊结尾
        print "started"
        m = 0
        for m in range(len(self.pmid)):  # 有多少重复多少
            author = str(self.author[m])[16:-4]  # 作者
            journal_end = str(self.journal[m]).find(journal_end_with) # 期刊结尾位置
            journal = str(self.journal[m])[26:journal_end].replace('<b>', '').replace('</b>', '')  # 期刊
            pmid = str(self.pmid[m])[4:-5]  # pmid
            title_start = str(self.title[m]).find(title_start_with) + 22
            title = str(self.title[m])[title_start:-8].replace('<b>', '').replace('</b>', '')  # 论文名
            issue = re.search("[1-2][09][0-9]{2}", str(self.issue[m])).group(0)  # 刊号
            if not(self.pmid_check(pmid)): # 如果之前没有这篇文章
                abstract = self.crawl_abstract(pmid) # 获取abstract和全文链接
                if abstract: # 如果能够返回正确的abstract，记录；否则留给下一次抓取（不记录，视作新论文）
                    record = author,issue,pmid,title,journal,abstract[0],abstract[1] #这里的abstract[0]是这篇文章的abstract,abstract[1]是全文下载的链接合集
                    self.data_write(record,"data") # 录入数据文件
                    self.pmid_write(pmid,"history") # 录入历史文件
                    print u" Retrieved !"
            else:
                print u" Skipped NO." + str(m+1) + u": Already retrieved"

    def crawl_abstract(self, pmid):  # 爬具体页面
        link = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
        full_content_links = [] # 全文链接（不是abstract，是可下载的pdf）
        full_links = [] # 原始全文链接的一个总集，需要处理到full_content_links里面
        tries = 3  # 尝试获取3次，不成功就返回错误
        while(tries > 0):
            try:
                opener = requests.Session()
                doc = opener.get(link, timeout=5, headers=headers).text
                soup = BeautifulSoup(doc)
                content = soup.findAll(name="abstracttext")
                abstract = str(content)
                full_content = soup.findAll(name='div', attrs={"class": "icons portlet"})
                full_links = re.findall("<a href=.*?ref=", str(full_content))
                if full_links:
                    for full_link in full_links:
                        full_content_links.append(full_link[9:-6].replace("&amp;", "&"))
                return abstract, full_content_links  # 返回的是一个值和一个集合
                break
            except Exception, e:
                tries -= 1
                print e
                print u"  Error: Cannot retrieve abstract; " + str(tries) + u" times left"
        else:
            print u"  Error: Abstract not available now"
            return 0

    def output(self, info, info_type="default"): # 所有的输出
        # 目前定义信息有这几种：default常规，error出错，warning警告，notice提示
        ISOTIMEFORMAT = '%Y-%m-%d %X' #设定了时间格式
        time_stamp = time.strftime( ISOTIMEFORMAT, time.localtime())
        msg = {'time':time_stamp,'project':self.project_name,'info':info,'info_type':info_type}
        return json.dumps(msg)

#=====================================================================================
# 实际爬的部分开始
    def crawl_direct(self): # 用于直接爬sum-page，只能爬第一页
        tries = 3 # 尝试3次
        while(tries > 0):
            try:
                opener = requests.Session()
                # opener.get(self.url, headers = headers)
                raw = opener.get(self.url, timeout=5, headers=headers).text
                soup = BeautifulSoup(raw)
                self.author = soup.findAll( name='p', attrs={"class": "desc"}) 
                self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})  
                self.title = soup.findAll(name='p', attrs={"class": "title"})  
                self.issue = soup.findAll(name="p", attrs={'class': 'details'}) 
                self.pmid = soup.findAll(name="dd") 
                self.generate_record() # 直接产生结果
                # print self.pmid
                break
            except Exception, e:
                tries -= 1
                print e
                print u" Error: Cannot retrieve sum page, trying again; " + str(tries) + u" times left"
                time.sleep(5)
        else:
            print u" Error: Sum page not available now"

    def crawl_phantom(self): # 用于使用phantomjs爬取sum-page，可以爬无限页，但是速度慢
        sum_page_number = self.sum_page_number # 总共需要多少sum-page
        time_out = 15 # 页面加载时间，预定15秒
        tries_first_sum_page = 2 # 尝试获取第一个页面的次数
        tries_other_sum_page = 3 # 尝试获取其它每个页面的次数
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
        dcap["phantomjs.page.settings.userAgent"] = (headers)  # header未来可以写成一个大集合，随机的
        dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
        browser = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器
        browser.set_page_load_timeout(time_out)  # 设定网页加载超时,超过了就不加载
        while (tries_first_sum_page > 0):
            try:
                browser.get(self.url)
                browser.implicitly_wait(5) # 等5秒钟，加载
                break
            except Exception as e:
                print e
                print "Retrying loading first sum page"
                tries_first_sum_page -= 1
        while(sum_page_number > 1):#确认需要第二页，如果sum-page只有1页，那就不用再打开
            while(tries_other_sum_page > 0):#尝试多少次，默认尝试3次，不行就打不开
                try:
                    browser.find_element_by_link_text("Next >").click() #直接就点开“下一页”，从第二页开始
                    browser.implicitly_wait(5) # 等5秒钟，加载
                    soup = BeautifulSoup(browser.page_source)
                    # self.content.append.str(soup.findAll(name="div", attrs={"class": "rslt"})) 
                    self.author = soup.findAll( name='p', attrs={"class": "desc"})  
                    self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})  
                    self.title = soup.findAll(name='p', attrs={"class": "title"})  
                    self.issue = soup.findAll(name="p", attrs={'class': 'details'}) 
                    self.pmid = soup.findAll(name="dd") 
                    self.generate_record() # 直接产生结果
                    sum_page_number -= 1
                    break
                except Exception as e:
                    browser.refresh() # 不行就刷新
                    browser.implicitly_wait(5) # 不行就等5秒重试
                    tries_other_sum_page -= 1
                    print e
            if tries_other_sum_page == 0:
                break
                print "Could not load page"
        browser.quit() # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能

if __name__ == '__main__':
    spider_test = Spider_pm("test", "dexter,chen", 80)
    spider_test.crawl_phantom()