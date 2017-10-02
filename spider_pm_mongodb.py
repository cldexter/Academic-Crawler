# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: spider_pm.py
   Description: 蜘蛛类，专用于pubmed
   Author: Dexter Chen
   Date：2018-08-25
-------------------------------------------------
   Development Note：
   爬虫蜘蛛的作用：传入关键词与数量 1.计算多少sum-page用phantomjs
   2.用request爬第一个sum-page 3.用phantomjs爬剩下的页面
   4.每爬一个页面（不管怎么爬的）都用BS4解析，获取基本信息
   5.判断是否为新 6.用request爬取abstract页面，用BS4解析
   7.储存论文 8.输出json
-------------------------------------------------
   Change Log:
   2017-08-26: 重写所有蜘蛛，使用面相对象的办法
   2017-08-29：抓取方法改为采用phantomjs + selenium
   2017-09-03: 把所有显示改写，改变模式
   2017-09-04: 重写抓取细节部分，机构可以抓取，关键词改为列表，修复csv空行
   2017-09-14: 把数据读写的放到data_handler.py中，避免重写
   2017-09-17: 更新了若干细节
   2017-10-01: 改为mongodb数据库
-------------------------------------------------
"""

from __future__ import division
import time
import sys
import re
import csv
import math

import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from BeautifulSoup import BeautifulSoup

import agents
import init
import mongodb_handler as mh
import journal as jn
import utilities as ut
import text_clean as tc


from data_handler import cur_file_dir

reload(sys)
sys.setdefaultencoding('utf8')


class Spider_pm:  # 爬虫的蜘蛛
    def __init__(self, project_name, key_words, record_number):
        self.key_words = key_words  # 输入关键词，关键词是一个集合
        self.record_number = record_number  # 需要爬多少个
        self.project_name = project_name  # 项目的名字
        self.run_type = 1  # 运行模式，如果用0，就是正常，1就是调试
        # 实例内部设定
        self.sum_page_number = int(
            math.ceil(self.record_number / 20))  # 每页20个，计算共多少页
        self.url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + \
            self.key_words.replace(",", "+")  # 最初的查询网址
        # 实例内部容器
        self.content = []  # 把sc_content类的抓过来；每次抓取新页面都清空
        self.author = []  # author合集；每次抓取新页面都清空
        self.journal = []  # 期刊合集；每次抓取新页面都清空
        self.title = []  # 名字与连接的合集；每次抓取新页面都清空
        self.issue = []  # 年份的合集；每次抓取新页面都清空
        self.pmid = []  # Pmid的合集；每次抓取新页面都清空
        self.output_msg = []  # 用于输出的信息json
        # 实例内部指示
        self.crawl_start_time = ""  # 什么时候项目开始的
        self.crawl_end_time = ""  # 项目什么时候结束的

        self.processed_sum_page = 0  # 处理过的
        self.processed_record = 0  # 处理过的数量
        self.suc_sum_page = 0  # 成功的页面数量
        self.suc_count = 0  # 成功的数量
        self.skip_sum_page = 0  # 失败的页面数量
        self.skip_count = 0  # 失败的数量

        # header随机换，但是
        self.headers = agents.get_header()

        self.pmid_set = mh.read_pmid_all()

#=====================================================================================
# 以下是需要的小函数
    def pmid_check(self, pmid):  # pmid在不在历史文件中，在，返回1；如果不在，返回0;用于防止抓多了
        if str(pmid) in self.pmid_set:
            return 1  # 如果有，说明是旧的
        else:
            return 0  # 如果没有，说明是新的

    def generate_record(self):  # 从抓取的原始素材产生记录
        title_start_with = "linksrc=docsum_title\">"  # 标记查找标题开头
        title_end_with = "</a>"  # 查找标题的结尾
        journal_start_with = 'title='  # 查找期刊开头
        journal_end_with = '\">'  # 查找期刊结尾
        m = 0
        while(m < len(self.pmid)):  # 有多少重复多少
            pmid = str(self.pmid[m])[4:-5]  # pmid
            self.processed_record += 1  # 标记已处理的数量
            m += 1
            if not(self.pmid_check(pmid)):  # 如果之前没有这篇文章
                author = str(self.author[m])[16:-4]
                author_list =  author.split(", ") # 作者
                journal_end = str(self.journal[m]).find(journal_end_with)  # 期刊结尾位置
                journal = str(self.journal[m])[26:journal_end].replace('<b>', '').replace('</b>', '')  # 期刊
                journal_detail = jn.journal_detail(journal)
                paper_detail = self.crawl_detail(pmid)  # 获取abstract和全文链接
                title_start = str(self.title[m]).find(title_start_with) + 22
                title = str(self.title[m])[title_start:-8].replace('<b>', '').replace('</b>', '')  # 论文名
                issue = re.search("[1-2][09][0-9]{2}", str(self.issue[m])).group(0)  # 刊号
                if paper_detail:  # 如果能够返回正确的abstract，记录；否则留给下一次抓取（不记录，视作新论文）
                    mh.add_new_content(self.project_name, self.key_words, ut.time_str("full"), "pm", pmid, title, author_list, journal, journal_detail[0], journal_detail[1], journal_detail[2], issue, str(paper_detail[0]), paper_detail[1], paper_detail[2], paper_detail[3])
                    self.pmid_set.append(pmid) # 把刚抓的这篇pmid加入pmid list
                    #这里的 paper_detail[0]是这篇文章的abstract,[1]是keywords,[2]是机构列表 [4]是全文下载的链接合集
                    self.suc_count += 1
                    if self.run_type:
                        print ut.time_str("time") + u"  INFO: Record NO." + str(self.processed_record) + " retrieved. Total retrieved: " + str(self.suc_count)
            else:
                self.skip_count += 1
                if self.run_type:
                    print ut.time_str("time") + u"  INFO: Record NO." + str(self.processed_record) + " skipped: already in. Total skipped: " + str(self.skip_count)


    def crawl_detail(self, pmid):  # 爬具体页面
        link = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
        full_links_list = []  # 全文链接（不是abstract，是可下载的pdf）
        institues_list = []  # 机构名称
        key_words_list = []  # 关键词合集
        # full_links_raw = [] # 原始全文链接的一个总集，需要处理到full_links_list里面
        tries = 3  # 尝试获取3次，不成功就返回错误
        while(tries > 0):
            try:
                opener = requests.Session()
                doc = opener.get(link, timeout=20, headers=agents.get_header()).text
                # 注意，这里是不断随机换agent的
                soup = BeautifulSoup(doc)
                abstract_raw = soup.findAll(name="abstracttext")
                abstract = tc.text_clean(str(abstract_raw))[1:-1]
                institues_raw = soup.findAll(name='dl')
                if institues_raw:
                    institues_raw = institues_raw[0]
                    institues_raw = re.findall("<dd>.*?</dd>", str(institues_raw))
                    for institues in institues_raw:
                            institues_list.append(institues[4:-5])
                full_content = soup.findAll(
                    name='div', attrs={"class": "icons portlet"})
                key_words_raw = soup.findAll(
                    name="div", attrs={"class": "keywords"})
                key_words_raw = str(key_words_raw)[45:-11].replace("; ", ";")
                if key_words_raw:
                    key_words_list = key_words_raw.split(';')
                full_links_raw = re.findall(
                    "<a href=.*?ref=", str(full_content))
                if full_links_raw:
                    for full_link in full_links_raw:
                        full_links_list.append(
                            full_link[9:-6].replace("&amp;", "&"))
                return abstract, key_words_list, institues_list, full_links_list  # 返回的是一个值和一个集合
                break
            except Exception, e:
                tries -= 1
                if self.run_type:
                    print e
                    print ut.time_str("time") + u"  ERROR: No detail for record NO." + str(self.processed_record) + "; " + str(tries) + u" tries left."
                time.sleep(3)  # 如果抓不成功，就先休息3秒钟
        else:
            if self.run_type:
                print ut.time_str("time") + u"  ERROR: Detail not available for record NO." + str(self.processed_record) + ", skipped. Total skipped: " + str(self.skip_count)
            return 0

    def project_sum(self):  # 所有的输出
        if self.processed_record == 0:
            print "  SUM: Project = " + self.project_name + " / Keywords = " + self.key_words
        print "  SUM: Record to scrawl: " + str(self.record_number) + " / Sum-page to scrawl: " + str(self.sum_page_number)
        if self.processed_record > 0:
            print "  SUM: Retrieved record " + str(self.suc_count) + " / Crawled pages " + str(self.suc_sum_page)
        print "  Start time: " + self.crawl_start_time
        if self.processed_record > 0:
            print "  End time: " + self.crawl_end_time

#=====================================================================================
# 实际爬的部分开始
    def crawl_direct(self):  # 用于直接爬sum-page，只能爬第一页
        sum_page_number = self.sum_page_number  # 总共需要多少sum-page
        self.crawl_start_time = ut.time_str()
        self.processed_sum_page += 1  # 处理1个sumpage
        tries = 2  # 尝试3次
        while(tries > 0):
            try:
                opener = requests.Session()
                # opener.get(self.url, headers = headers)
                raw = opener.get(self.url, timeout=20,
                                 headers=self.headers).text
                if self.run_type:
                    self.project_sum()
                    print ut.time_str("time") + u"  INFO: Sum-page NO.1 is loaded in Requests. Total loaded: " + str(self.suc_sum_page + 1)
                soup = BeautifulSoup(raw)
                max_sum_page_number_raw = soup.findAll(
                    name="input", attrs={"id": "pageno"})
                number_start = str(max_sum_page_number_raw).find(
                    "last=") + 6  # 找到总数开始位置
                number_end = str(max_sum_page_number_raw).find(
                    "\" />")  # 找到总数结束位置
                max_sum_page_number = int(str(max_sum_page_number_raw)[
                                          number_start:number_end])  # 实际最大数值,整数
                if max_sum_page_number < sum_page_number:
                    self.sum_page_number = max_sum_page_number  # 如果实际最大页面数没有计算值大，那用实际值，否则不变
                    if self.run_type:
                        print ut.time_str("time") + u"  NOTICE: Max page number changed:" + str(max_sum_page_number)
                self.author = soup.findAll(name='p', attrs={"class": "desc"})
                self.journal = soup.findAll(
                    name="span", attrs={'class': 'jrnl'})
                self.title = soup.findAll(name='p', attrs={"class": "title"})
                self.issue = soup.findAll(name="p", attrs={'class': 'details'})
                self.pmid = soup.findAll(name="dd")
                self.generate_record()  # 直接产生结果
                self.suc_sum_page += 1
                break
            except Exception, e:
                tries -= 1
                if self.run_type:
                    print e
                    print ut.time_str("time") + u"  ERROR: Cannot retrieve sum-page NO." + str(self.processed_sum_page) + "; " + str(tries) + u" tries left."
                time.sleep(0)
        else:
            if self.run_type:
                print ut.time_str("time") + u"  ERROR: Sum-page NO." + str(self.processed_sum_page) + " not available now."

    def crawl_phantom(self):  # 用于使用phantomjs爬取sum-page，可以爬无限页，但是速度慢
        sum_page_number = self.sum_page_number
        time_out = 60  # 页面加载时间，预定最多30秒
        tries_first_sum_page = 5  # 尝试获取第一个页面的次数
        if self.sum_page_number > 1:
            dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
            dcap["phantomjs.page.settings.userAgent"] = (
                self.headers)  # header未来可以写成一个大集合，随机的
            dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
            # browser = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器，windows下使用
            path = cur_file_dir() + "/browser/phantomjs"
            browser = webdriver.PhantomJS(
                executable_path=path, desired_capabilities=dcap)  # 加载浏览器
            browser.set_page_load_timeout(60)  # 设定网页加载超时,超过了就不加载
            if self.run_type:
                print ut.time_str("time") + "  INFO: Loading NO.1 sum-page in PhantomJS."
        while (self.sum_page_number > 1 and tries_first_sum_page > 0):
            try:
                browser.get(self.url)
                if self.run_type:
                    print ut.time_str("time") + u"  INFO: NO." + str(self.processed_sum_page) + u" loaded. Total loaded: " + str(self.suc_sum_page)
                WebDriverWait(browser, 60).until(
                    EC.presence_of_element_located((By.ID, "footer")))
                break
            except Exception as e:
                tries_first_sum_page -= 1
                if self.run_type:
                    print e
                    print ut.time_str("time") + u"  ERROR: Sum-page NO.1 not available in PhatomJS; " + str(tries_first_sum_page) + " tries left."
                    print ut.time_str("time") + u"  NOTICE: Browser refreshed, wait for 5 secs to retry."
                browser.refresh()
                browser.implicitly_wait(5)
                # browser.save_screenshot("log.png")
        while(sum_page_number > 1 and tries_first_sum_page > 1):  # 确认需要第二页，如果sum-page只有1页，那就不用再打开
            # 从这里开始循环，直到所有的页面都爬完为止
            self.processed_sum_page += 1
            tries_other_sum_page = 5  # 尝试获取其它每个页面的次数，每次循环还原成5次（不累积）
            if self.run_type:
                print ut.time_str("time") + "  INFO: Loading NO." + str(self.processed_sum_page) + " sum-page in PhantomJS."
            while(tries_other_sum_page > 0):  # 尝试多少次，默认尝试3次，不行就打不开
                try:
                    browser.find_element_by_link_text(
                        "Next >").click()  # 直接就点开“下一页”，从第二页开始
                    WebDriverWait(browser, time_out).until(
                        EC.presence_of_element_located((By.ID, "footer")))
                    # browser.implicitly_wait(5) # 等5秒钟，加载
                    if self.run_type:
                        print ut.time_str("time") + u"  INFO: Sum-page NO." + str(self.processed_sum_page) + u" loaded in PhantomJS. Total loaded: " + str(self.suc_sum_page + 1)
                    soup = BeautifulSoup(browser.page_source)
                    self.author = soup.findAll(
                        name='p', attrs={"class": "desc"})
                    self.journal = soup.findAll(
                        name="span", attrs={'class': 'jrnl'})
                    self.title = soup.findAll(
                        name='p', attrs={"class": "title"})
                    self.issue = soup.findAll(
                        name="p", attrs={'class': 'details'})
                    self.pmid = soup.findAll(name="dd")
                    self.generate_record()  # 直接产生结果
                    self.suc_sum_page += 1
                    sum_page_number -= 1
                    break
                except Exception as e:
                    tries_other_sum_page -= 1
                    if self.run_type:
                        print e
                        print ut.time_str("time") + u"  ERROR: Sum-page NO." + str(self.processed_sum_page) + u" not available in PhantomJS; " + str(tries_other_sum_page) + " tries left."
                        print ut.time_str("time") + u"  NOTICE: Browser refreshed, now wait for 5 secs to retry."
                    browser.refresh()  # 不行就刷新
                    browser.implicitly_wait(5)  # 不行就等5秒重试
            if tries_other_sum_page == 0:
                break
                if self.run_type:
                    print ut.time_str("time") + u"  ERROR: Sum-page NO." + str(self.processed_sum_page) + "not available now. Program terminated."
        if self.sum_page_number > 1:
            browser.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能
        self.crawl_end_time = ut.time_str()
        if self.run_type:
            self.project_sum()

    def crawl_run(self):
        self.crawl_direct()  # 先爬第一sum-page
        self.crawl_phantom()  # 爬剩下的所有页


if __name__ == '__main__':
    spider_test = Spider_pm("cancer", "breast,cancer", 200)
    spider_test.crawl_run()