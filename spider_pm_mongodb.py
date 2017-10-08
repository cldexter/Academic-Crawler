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
import message as msg
import stats


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

        # self.processed_sum_page = 0  # 处理过的
        # self.processed_record = 0  # 处理过的数量
        # self.suc_sum_page = 0  # 成功的页面数量
        # self.suc_count = 0  # 成功的数量
        # self.skip_sum_page = 0  # 失败的页面数量
        # self.skip_count = 0  # 失败的数量

        # header随机换，但是
        self.headers = agents.get_header() # 随机选择一个以供浏览器使用

        self.pmid_set = mh.read_pmid_all() # 只读一次

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
            pmid = str(self.pmid[m])[4:-5]  # 先找到pmid，再决定要不要下一步
            # self.processed_record += 1  # 标记已处理的数量
            if not(self.pmid_check(pmid)):  # 如果之前没有这篇文章
                author = str(self.author[m])[16:-4]
                author_list =  author.split(", ") # 作者列表
                title_start = str(self.title[m]).find(title_start_with) + 22
                title = str(self.title[m])[title_start:-8].replace('<b>', '').replace('</b>', '')  # 论文名
                issue = re.search("[1-2][09][0-9]{2}", str(self.issue[m])).group(0)  # 刊号，即年份
                journal_end = str(self.journal[m]).find(journal_end_with)  # 期刊结尾位置
                journal = str(self.journal[m])[26:journal_end].replace('<b>', '').replace('</b>', '')  # 期刊名
                journal_detail = jn.journal_detail(journal) # 获取期刊的正式名称，影响因子及分区信息
                paper_detail = self.crawl_detail(pmid)  # 获取文章abstract，keyword列表，机构列表和全文链接列表
                if paper_detail:  # 如果能够返回正确的abstract，记录；否则留给下一次抓取（不记录，视作新论文）
                    mh.add_new_content(self.project_name, self.key_words, ut.time_str("full"), "pm", pmid, title, author_list, journal, journal_detail[0], journal_detail[1], journal_detail[2], issue, str(paper_detail[0]), paper_detail[1], paper_detail[2], paper_detail[3])
                    self.pmid_set.append(pmid) # 把刚抓的这篇pmid加入pmid list
                    #这里的 paper_detail[0]是这篇文章的abstract,[1]是keywords,[2]是机构列表 [4]是全文下载的链接合集
                    msg.stat("record", "succ") # 统计：记录成功
                    msg.display(ut.time_str("time"), "retrieved record: " + str(pmid) + "; total retrieved: " + str(stats.success_record), "info") # 显示：记录成功
                    msg.log("", ut.time_str("time"), "retrieved record: " + str(pmid), "info") # 记录：记录成功
            else:
                msg.stat("record", "skip")
                msg.display(ut.time_str("time"), "skipped record: " + str(pmid) + "; total skipped: " + str(stats.skipped_record), "info")
                msg.log("", ut.time_str("time"), "skipped record: " + str(pmid), "info")
            m += 1    

    def crawl_detail(self, pmid):  # 爬具体页面
        link = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
        key_words_list = []  # 关键词合集
        institues_list = []  # 机构名称
        full_links_list = []  # 全文链接（不是abstract，是可下载的pdf）

        tries = 3  # 尝试获取3次，不成功就返回错误
        while(tries > 0):
            try:
                opener = requests.Session()
                doc = opener.get(link, timeout=20, headers=agents.get_header()).text # 注意，这里是不断随机换agent的
                soup = BeautifulSoup(doc)
                abstract_raw = soup.findAll(name="abstracttext")
                abstract = ut.regexp_replace(str(abstract_raw),ut.re_html)[1:-1] # 即时清理abstract
                full_content = soup.findAll(name='div', attrs={"class": "icons portlet"})                
                
                key_words_raw = soup.findAll(name="div", attrs={"class": "keywords"})
                if key_words_raw: # 如果有keyword的话，很多文章是没有
                    key_words_raw = str(key_words_raw)[45:-11].replace("; ", ";")
                    key_words_list = key_words_raw.split(';')
                
                institues_raw = soup.findAll(name='dl')
                if institues_raw: # 如果有institues的话，大部分文章都有
                    institues_raw = institues_raw[0]
                    institues_raw = re.findall("<dd>.*?</dd>", str(institues_raw))
                    for institues in institues_raw:
                        institues_list.append(institues[4:-5])
                    
                full_links_raw = re.findall("<a href=.*?ref=", str(full_content))
                if full_links_raw: # 如果有全文链接
                    for full_link in full_links_raw:
                        full_links_list.append(full_link[9:-6].replace("&amp;", "&"))

                return abstract, key_words_list, institues_list, full_links_list  # 返回的是一个str值和3个集合
                break
            except Exception, e:
                tries -= 1
                msg.display(ut.time_str("time"), "retrying record: " + str(pmid) + "; " + str(tries) + " tries left", "notice")
                msg.log("", ut.time_str("time"), "retry record: " + str(pmid), "notice")
                msg.log("", ut.time_str("time"), str(e), "error")
                time.sleep(3)  # 如果抓不成功，就先休息3秒钟
        else:
            msg.display(ut.time_str("time"), "retrieve record fail: " + str(pmid), "error")
            msg.log("", ut.time_str("time"), "failed record: " + str(pmid), "error")
            msg.stat("record", "fail")
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
        self.crawl_start_time = ut.time_str()
        # self.processed_sum_page += 1  # 处理1个sumpage
        tries = 3  # 尝试3次
        while(tries > 0):
            try:
                # self.project_sum()
                opener = requests.Session()
                raw = opener.get(self.url, timeout=20, headers=self.headers).text              
                soup = BeautifulSoup(raw)

                max_sum_page_number_raw = soup.findAll(name="input", attrs={"id": "pageno"}) # 找到含总数的div
                number_start = str(max_sum_page_number_raw).find("last=") + 6  # 找到总数开始位置
                number_end = str(max_sum_page_number_raw).find("\" />")  # 找到总数结束位置
                max_sum_page_number = int(str(max_sum_page_number_raw)[number_start:number_end])  # 实际最大数值,整数

                if max_sum_page_number < self.sum_page_number: # 如果实际最大页面数没有计算值大
                    self.sum_page_number = max_sum_page_number  # 那用实际值，否则不变
                    msg.display(ut.time_str("time"), "max sum page changed: " + str(max_sum_page_number), "notice")  
                    msg.log("", ut.time_str("time"), "max sum page changed: " + str(max_sum_page_number), "notice")

                msg.display(ut.time_str("time"), "loaded: NO.1 sum page (requests)", "info") 
                msg.log("", ut.time_str("time"), "loaded sum page: NO.1 (requests)", "info")
                msg.stat("sum_page", "succ")

                self.author = soup.findAll(name='p', attrs={"class": "desc"})
                self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})
                self.title = soup.findAll(name='p', attrs={"class": "title"})
                self.issue = soup.findAll(name="p", attrs={'class': 'details'})
                self.pmid = soup.findAll(name="dd")

                self.generate_record()  # 直接产生结果
                # self.suc_sum_page += 1

                break
            except Exception, e:
                print e
                tries -= 1
                msg.display(ut.time_str("time"), "load retrying: NO.1 sum page (requests); " + str(tries) + " tries left", "notice")
                msg.log("", ut.time_str("time"), "retry sum page: NO.1 (requests)", "notice")
                msg.log("", ut.time_str("time"), str(e), "error")
                
        else:
            msg.display(ut.time_str("time"), "load failed: NO.1 sum page (request)", "error")
            msg.log("", ut.time_str("time"), "fail sum page: NO.1 (request)", "error")
            msg.stat('sum_page', "fail")
            

    def crawl_phantom(self):  # 用于使用phantomjs爬取sum-page，可以爬无限页，但是速度慢
        sum_page_number = self.sum_page_number
        time_out = 60  # 页面加载时间，预定最多30秒
        tries_first_sum_page = 3  # 尝试获取第一个页面的次数

        if self.sum_page_number > 1: # 如果页面不超过1个，就根本不启动浏览器
            dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
            dcap["phantomjs.page.settings.userAgent"] = (self.headers)  # header未来可以写成一个大集合，随机的
            dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
            # browser = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器，windows下使用
            path = cur_file_dir() + "/browser/phantomjs" # 浏览器地址
            browser = webdriver.PhantomJS(executable_path=path, desired_capabilities=dcap)  # 加载浏览器
            browser.set_page_load_timeout(time_out)  # 设定网页加载超时,超过了就不加载
        while (self.sum_page_number > 1 and tries_first_sum_page > 0):
            try:
                browser.get(self.url)
                WebDriverWait(browser, time_out).until(EC.presence_of_element_located((By.ID, "footer")))
                msg.display(ut.time_str("time"), "loaded: NO.1 sum page (phantomjs)", "info")
                msg.log("", ut.time_str("time"), "loaded sum page: NO.1 (phantomjs)", "info")                
                break
            except Exception as e:
                tries_first_sum_page -= 1
                msg.display(ut.time_str("time"), "load retrying: NO.1 sum page (phantomjs); " + str(tries_first_sum_page) + " tries left", "notice")
                msg.log("", ut.time_str("time"), "retry loading NO.1 sum page in (phantomjs)", "notice")
                msg.log("", ut.time_str("time"), str(e), "error")
                browser.refresh()
                browser.implicitly_wait(5)
        while(sum_page_number > 1 and tries_first_sum_page > 0):  # 确认需要第二页，如果sum-page只有1页，那就不用再打开; 如果第一页打开失败，也不用打开；从这里开始循环，直到所有的页面都爬完为止
            # self.processed_sum_page += 1
            tries_other_sum_page = 5  # 尝试获取其它每个页面的次数，每次循环还原成5次（不累积）
            
            while(tries_other_sum_page > 0):  # 尝试多少次，默认尝试5次，不行就打不开
                try:
                    browser.find_element_by_link_text("Next >").click()  # 直接就点开“下一页”，从第二页开始
                    WebDriverWait(browser, time_out).until(EC.presence_of_element_located((By.ID, "footer")))
                    
                    msg.display(ut.time_str("time"), "loading NO." + str(stats.processed_sum_page) + " page in Phantomjs", "notice")   
                    msg.log("", ut.time_str("time"), "loading NO." + str(stats.processed_sum_page) + " page in Phantomjs", "notice")
                                      
                    soup = BeautifulSoup(browser.page_source)
                    self.author = soup.findAll(name='p', attrs={"class": "desc"})
                    self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})
                    self.title = soup.findAll(name='p', attrs={"class": "title"})
                    self.issue = soup.findAll(name="p", attrs={'class': 'details'})
                    self.pmid = soup.findAll(name="dd")
                    self.generate_record()  # 直接产生结果

                    # self.suc_sum_page += 1
                    sum_page_number -= 1
                    break
                except Exception as e:
                    tries_other_sum_page -= 1
                    msg.log("", ut.time_str("time"), "retrying loading NO." + str(stats.processed_sum_page) + " page in Phantomjs", "error")
                    msg.log("", ut.time_str("time"), str(e), "error")
                    msg.display(ut.time_str("time"), "retrying loading NO." + str(stats.processed_sum_page) + " page in Phantomjs; " + str(tries_other_sum_page) + " tries left.", "error")
                    browser.refresh()  # 不行就刷新
                    browser.implicitly_wait(5)  # 不行就等5秒重试

            if tries_other_sum_page == 0:
                break
                msg.log("", ut.time_str("time"), "failed NO." + str(stats.processed_sum_page) + " page in Phantomjs", "error")
                msg.display(ut.time_str("time"), "failed NO." + str(stats.processed_sum_page) + " page in Phantomjs", "error")
        if self.sum_page_number > 1:
            browser.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS

        # self.crawl_end_time = ut.time_str()
        # if self.run_type:
        #     self.project_sum()

    def crawl_run(self):
        self.crawl_direct()  # 先爬第一sum-page
        self.crawl_phantom()  # 爬剩下的所有页


if __name__ == '__main__':
    spider_test = Spider_pm("cancer", "breast,cancer", 200)
    spider_test.crawl_direct()