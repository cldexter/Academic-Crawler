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

class Spider_pm:  # 爬虫的蜘蛛
    def __init__(self, key_words, record_number, project_name):
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

        self.abstract_page_url = []  # abstract 链接的合集；每次抓取新页面都清空
        
        self.output_msg = []  # 用于输出的信息json

        self.record = [] # 用于数据临时存储； 不清空，可无限添加

#=====================================================================================
# 以下是需要的小函数

    def pmid_read(self, file_type):  # 读取pmid库，自动关闭文件
        with open(file_name(self.project_name, file_type), 'r') as f:
            pmid_set = f.read()
        return pmid_set

    def pmid_write(self, pmid, file_type):  # 存入pmid,自动关闭文件
        with open(file_name(self.project_name, file_type), "a") as f:
            f.write(pmid + ',')

    def check_pmid(self, pmid):  # pmid在不在历史文件中，在，返回1；如果不在，返回0;用于防止抓多了
        pmid_set = pmid_read(self.project_name, "history")
        if pmid in pmid_set:
            return 1  # 如果有，说明是旧的
        else:
            return 0  # 如果没有，说明是新的

    def generate_record(self): # 从抓取的原始素材产生记录
        m = 0
        n = 0
        title_start_with = "linksrc=docsum_title\">"#标记查找标题开头
        title_end_with = "</a>"#查找标题的结尾
        journal_start_with = 'title='#查找期刊开头
        journal_end_with = '\">'#查找期刊结尾
        for m in range(len(self.content)):  # 有多少重复多少
            author[m] = str(self.author[m])[16:-4]  # 作者
            journal_end = str(self.journal[m]).find(journal_end_with)
            journal[m] = str(self.journal[m])[26:journal_end].replace('<b>', '').replace('</b>', '')  # 期刊
            pmid[m] = str(self.pmid[m])[4:-5]  # pmid
            title_start = str(self.title[m]).find(title_start_with) + 22
            title[m] = str(self.title[m])[title_start:-8].replace('<b>', '').replace('</b>', '')  # 论文名
            issue[m] = re.search("[1-2][09][0-9]{2}", str(self.issue[m])).group(0)  # 刊号
            if not(check_pmid(pmid[m])): # 如果之前没有这篇文章
                abstract = crawl_abstract_page(pmid[m]) # 获取abstract
                if abstract: # 如果能够返回正确的abstract，记录；否则留给下一次抓取（不记录，视作新论文）
                record = author[m],issue[m],pmid[m],title[m],journal[m],abstract[0],abstract[1] #这里的abstract[0]是这篇文章的abstract,abstract[1]是全文下载的链接合集
                data_write(record,self.project_name,"data") # 录入数据文件
                pmid_write(pmid[m],self.project_name,"history") # 录入历史文件
                n += 1  # 记录多少篇新文章
                print u"  New: " + str(title[m])  # 录入
                time.sleep(5)
            else:
                print u" ○ Skipped NO." + str(m+1) + u": Already retrieved"
        print u"  Retrieved " + str(n) + u" new articles"

    def crawl_abstract_page(self, pmid):  # 爬具体页面
        link = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
        full_content_links = [] # 全文链接（不是abstract，是可下载的pdf）
        full_links = [] #
        tries = 3  # 尝试获取3次，不成功就返回错误
        while(tries > 0):
            try:
                opener = requests.Session()
                doc = opener.get(link, timeout=5, headers=headers).text
                soup = BeautifulSoup(doc)
                content = soup.findAll(name="abstracttext")
                abstract = str(content)
                full_content = soup.findAll(
                    name='div', attrs={"class": "icons portlet"})
                full_links = re.findall("<a href=.*?ref=", str(full_content))
                if full_links:
                    for full_link in full_links:
                        full_content_links.append(full_link[9:-6].replace("&amp;", "&"))
                return abstract, full_content_links  # 返回的是一个值和一个集合
                break
            except Exception, e:
                tries -= 1
                print u"  Error: Cannot retrieve abstract; " + str(tries) + u" times left"
        else:
            print u"  Error: Abstract not available now"
            return 0
#=====================================================================================


    def crawl_sum_page_direct(self): # 用于直接爬sum-page，只能爬第一页
        tries = 3 # 尝试3次
        while(tries > 0):
            try:
                opener = requests.Session()
                opener.get(self.url, headers=headers)
                doc = opener.get(self.url, timeout=5, headers=headers).text
                soup = BeautifulSoup(doc)
                self.content.append.str(soup.findAll(
                    name="div", attrs={"class": "rslt"})) 
                self.author = soup.findAll(
                    name='p', attrs={"class": "desc"})  
                self.journal = soup.findAll(
                    name="span", attrs={'class': 'jrnl'})  
                self.title = soup.findAll(
                    name='p', attrs={"class": "title"})  
                self.issue = soup.findAll(
                    name="p", attrs={'class': 'details'}) 
                self.pmid = soup.findAll(name="dd") 
                generate_record() # 直接产生结果
                break
            except Exception, e:
                tries -= 1
                print u" Error: Cannot retrieve sum page, trying again; " + str(tries) + u" times left"
                time.sleep(5)
        else:
            print u" Error: Sum page not available now"

    def crawl_sum_page_phantom(self,sum_page_number): # 用于使用phantomjs爬取sum-page，可以爬无限页，但是速度慢
        time_out = 30
        tries = 3
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
        dcap["phantomjs.page.settings.userAgent"] = (headers)  # header未来可以写成一个大集合，随机的
        dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
        obj = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器
        obj.set_page_load_timeout(time_out)  # 设定网页加载超时
        # obj.set_window_size('1024', '1280')  # 设定虚拟浏览器窗口大小
        
        while(tries > 0):
            try:
                obj.get(self.url)  # 打开网址
                while(self.sum_page_number > 0):
                    obj.find_element_by_link_text("Next >").click() #直接就点开“下一页”，从第二页开始
                    soup = BeautifulSoup(obj.page_source)
                    self.content.append.str(soup.findAll(name="div", attrs={"class": "rslt"})) 
                    self.author = soup.findAll(name='p', attrs={"class": "desc"})  
                    self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})  
                    self.title = soup.findAll(name='p', attrs={"class": "title"})  
                    self.issue = soup.findAll(name="p", attrs={'class': 'details'}) 
                    self.pmid = soup.findAll(name="dd") 
                    generate_record() # 直接产生结果
                    
                break
            except Exception as e:
                print "Retry " + str(i) + " time"
                print e
                tries -= 1
        if i == tries:
            print " Error: Cannot connect to the server"
        obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能



    def record(self,):  # 记录格式是json
        pass

    def output(self, msg):  # 输出信息都用json格式
        pass


if __name__ == '__main__':
    spider_test = Spider_pm("dexter,chen", 20)
    spider_test.sum_page_url()
    spider_test.crawl_sum_page_1st()
