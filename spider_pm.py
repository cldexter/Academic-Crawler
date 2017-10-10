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
"""

from __future__ import division
import time
import sys
import re
import math

import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from BeautifulSoup import BeautifulSoup
from data_handler import cur_file_dir

import agents
import mongodb_handler as mh
import journal as jn
import utilities as ut
import message as msg
import stats

reload(sys)
sys.setdefaultencoding('utf8')


class Spider_pm:  # 爬虫的蜘蛛
    def __init__(self, task_name, project_name, key_words, record_number):
        self.key_words = key_words  # 输入关键词，关键词是一个集合
        self.record_number = record_number  # 需要爬多少个
        self.project_name = project_name  # 项目的名字
        self.task_name = task_name

        self.request_time_out = 30 # request超时时间
        self.phantomjs_time_out = 60 # phantom超时时间
        self.request_refresh_wait = 3 # request刷新等待
        self.phantomjs_refresh_wait = 5 # 浏览器刷新等待

        self.tries_request = 3
        self.tries_1st_sp = 3  # 尝试获取第一个页面的次数
        self.tries_other_sp = 5  # 尝试获取其它每个页面的次数

        self.sum_page_number = int(math.ceil(self.record_number / 20))  # 每页20个，计算共多少页
        self.url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + self.key_words.replace(",", "+")  # 最初的查询网址

        self.phantomjs_headers = agents.get_header() # 随机选择一个以供浏览器使用
        self.pmid_set = mh.read_pmid_all() # 只读一次

        # 实例内部容器
        self.content = []  # 把sc_content类的抓过来；每次抓取新页面都清空
        self.author = []  # author合集；每次抓取新页面都清空
        self.journal = []  # 期刊合集；每次抓取新页面都清空
        self.title = []  # 名字与连接的合集；每次抓取新页面都清空
        self.issue = []  # 年份的合集；每次抓取新页面都清空
        self.pmid = []  # Pmid的合集；每次抓取新页面都清空


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
            msg.stat("record", "proc") # 处理记录+1
            pmid = str(self.pmid[m])[4:-5]  # 先找到pmid，再决定要不要下一步
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
                    msg.stat("record", "succ") # 记录成功+1
                    msg.display(ut.time_str("time"), "retrieved record: " + str(pmid) + "; total retrieved: " + str(stats.success_record), "info") # 显示：记录成功
                    msg.log(self.task_name, ut.time_str("full"), "retrieved record: " + str(pmid), "info") # 记录：记录成功
            else:
                msg.stat("record", "skip") # 跳过记录+1
                msg.display(ut.time_str("time"), "skipped record: " + str(pmid) + "; total skipped: " + str(stats.skipped_record), "info")
                msg.log(self.task_name, ut.time_str("full"), "skipped record: " + str(pmid), "info")
            m += 1    

    def crawl_detail(self, pmid):  # 爬具体页面
        link = "https://www.ncbi.nlm.nih.gov/pubmed/" + pmid
        key_words_list = []  # 关键词合集
        institues_list = []  # 机构名称
        full_links_list = []  # 全文链接（不是abstract，是可下载的pdf）

        tries = 3  # 尝试获取3次，不成功就返回错误
        while(tries > 0):
            try:
                opener = requests.Session() # 新建了session保存
                doc = opener.get(link, timeout=self.request_time_out, headers=agents.get_header()).text # 注意，这里是不断随机换agent的
                soup = BeautifulSoup(doc)

                abstract_raw = soup.findAll(name="abstracttext")
                abstract = ut.regexp_replace(str(abstract_raw),ut.re_html)[1:-1] # 即时清理abstract
                              
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

                full_content = soup.findAll(name='div', attrs={"class": "icons portlet"})      
                full_links_raw = re.findall("<a href=.*?ref=", str(full_content))
                if full_links_raw: # 如果有全文链接
                    for full_link in full_links_raw:
                        full_links_list.append(full_link[9:-6].replace("&amp;", "&"))

                return abstract, key_words_list, institues_list, full_links_list  # 返回的是一个str值和3个集合
                break
            
            except Exception, e:
                tries -= 1
                msg.display(ut.time_str("time"), "retrying record: " + str(pmid) + "; " + str(tries) + " tries left", "notice")
                msg.log(self.task_name, ut.time_str("full"), "retry record: " + str(pmid), "notice")
                msg.log(self.task_name, ut.time_str("full"), str(e), "error")
                time.sleep(self.request_refresh_wait)  # 如果抓不成功，就先休息3秒钟
        
        else:
            msg.display(ut.time_str("time"), "retrieve record fail: " + str(pmid), "error")
            msg.log(self.task_name, ut.time_str("full"), "failed record: " + str(pmid), "error")
            msg.stat("record", "fail")
            return 0


#=====================================================================================
# 实际爬的部分开始
    def crawl_direct(self):  # 用于直接爬sum-page，只能爬第一页，但是不采用phantomjs，速度快
        msg.stat("sum_page", "proc") # 列入已处理
        tries = self.tries_request # 尝试3次
        while(tries > 0):
            try:
                opener = requests.Session()
                raw = opener.get(self.url, timeout=self.request_time_out, headers=agents.get_header()).text # header仍然可以是随机的              
                soup = BeautifulSoup(raw)

                number_raw = soup.findAll(name="input", attrs={"id": "pageno"}) # 找到含总数的div
                number_start = str(number_raw).find("last=") + 6  # 找到总数开始位置
                number_end = str(number_raw).find("\" />")  # 找到总数结束位置
                max_number = int(str(number_raw)[number_start:number_end])  # 实际最大数值,整数

                if max_number < self.sum_page_number: # 如果实际最大页面数没有计算值大
                    self.sum_page_number = max_number  # 那用实际值，否则不变
                    msg.display(ut.time_str("time"), "max sum page changed: " + str(max_number), "notice")  
                    msg.log(self.task_name, ut.time_str("full"), "changed sum page number: " + str(max_number), "notice")
                
                msg.display(ut.time_str("time"), "loaded: NO.1 sum page (requests)", "info") 
                msg.log(self.task_name, ut.time_str("full"), "load sum page: NO.1 (requests)", "info")

                self.author = soup.findAll(name='p', attrs={"class": "desc"})
                self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})
                self.title = soup.findAll(name='p', attrs={"class": "title"})
                self.issue = soup.findAll(name="p", attrs={'class': 'details'})
                self.pmid = soup.findAll(name="dd")

                self.generate_record()  # 直接产生结果
                msg.stat("sum_page", "succ")
                break
            
            except Exception, e:
                print e
                tries -= 1
                msg.display(ut.time_str("time"), "load retrying: NO.1 sum page (requests); " + str(tries) + " tries left", "notice")
                msg.log(self.task_name, ut.time_str("full"), "retry sum page: NO.1 (requests)", "notice")
                msg.log(self.task_name, ut.time_str("full"), str(e), "error")
                
        else:
            msg.stat('sum_page', "fail")
            msg.display(ut.time_str("time"), "load failed: NO.1 sum page (request)", "error")
            msg.log(self.task_name, ut.time_str("full"), "fail sum page: NO.1 (request)", "error")
            
            

    def crawl_phantom(self):  # 用于使用phantomjs爬取sum-page，可以爬无限页，但是速度慢
        rest_page_number = self.sum_page_number # 剩下多少页
        tries_1st_sp = self.tries_1st_sp
        tries_other_sp = self.tries_other_sp
        
        if self.sum_page_number > 1: # 如果页面不超过1个，就不启动浏览器
            dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
            dcap["phantomjs.page.settings.userAgent"] = (self.phantomjs_headers)  # header每次打开phantomjs是随机的，但浏览器关闭前不会变
            dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
            # browser = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器，windows下使用
            path = cur_file_dir() + "/browser/phantomjs" # 浏览器地址
            browser = webdriver.PhantomJS(executable_path=path, desired_capabilities=dcap)  # 加载浏览器
            browser.set_page_load_timeout(self.phantomjs_time_out)  # 设定网页加载超时,超过了就不加载

        while (self.sum_page_number > 1 and tries_1st_sp > 0):
            try:
                browser.get(self.url)
                WebDriverWait(browser, self.phantomjs_time_out).until(EC.presence_of_element_located((By.ID, "footer")))
                msg.display(ut.time_str("time"), "loaded: NO.1 sum page (phantomjs)", "info")
                msg.log(self.task_name, ut.time_str("full"), "load sum page: NO.1 (phantomjs)", "info") 
                msg.stat("sum_page", "succ")              
                break

            except Exception as e:
                tries_1st_sp -= 1
                msg.display(ut.time_str("time"), "load retrying: NO.1 sum page (phantomjs); " + str(tries_1st_sp) + " tries left", "notice")
                msg.log(self.task_name, ut.time_str("full"), "retry sum page: NO.1 (phantomjs)", "notice")
                msg.log(self.task_name, ut.time_str("full"), str(e), "error")

                browser.refresh()
                browser.implicitly_wait(self.phantomjs_refresh_wait)

        else:
            msg.display(ut.time_str("time"), "load failed: NO.1 sum page (phantomjs)", "error")
            msg.log(self.task_name, ut.time_str("full"), "fail sum page: NO.1 (phantomjs)", "error")


        while(rest_page_number > 1 and tries_1st_sp > 0):  # 确认需要第二页，如果sum-page只有1页，那就不用再打开; 如果第一页打开失败，也不用打开；从这里开始循环，直到所有的页面都爬完为止
            msg.stat("sum_page", "proc")
            tries_other_sp = self.tries_other_sp
            
            while(tries_other_sp > 0):  # 尝试多少次，默认尝试5次，不行就打不开
                try:
                    browser.find_element_by_link_text("Next >").click()  # 直接就点开“下一页”，从第二页开始
                    WebDriverWait(browser, self.phantomjs_time_out).until(EC.presence_of_element_located((By.ID, "footer")))
                    
                    msg.display(ut.time_str("time"), "loaded: NO." + str(stats.success_sum_page + 1) + " sum page (phantomjs)", "info")   
                    msg.log(self.task_name, ut.time_str("full"), "load sum page: NO." + str(stats.success_sum_page + 1) + " (phantomjs)", "info")
                                      
                    soup = BeautifulSoup(browser.page_source)
                    self.author = soup.findAll(name='p', attrs={"class": "desc"})
                    self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})
                    self.title = soup.findAll(name='p', attrs={"class": "title"})
                    self.issue = soup.findAll(name="p", attrs={'class': 'details'})
                    self.pmid = soup.findAll(name="dd")
                    self.generate_record()  # 直接产生结果

                    msg.stat("sum_page", "succ")
                    rest_page_number -= 1
                    break
                
                except Exception as e:
                    tries_other_sp -= 1
                    msg.display(ut.time_str("time"), "load retrying: NO." + str(stats.success_sum_page + 1) + " sum page (phantomjs); " + str(tries_other_sp) + " tries left", "notice")
                    msg.log(self.task_name, ut.time_str("full"), "retry sum page: NO." + str(stats.success_sum_page + 1) + " (phantomjs)", "notice")
                    msg.log(self.task_name, ut.time_str("full"), str(e), "error")
                    
                    browser.refresh()
                    browser.implicitly_wait(self.phantomjs_refresh_wait)

            else:
                msg.stat("sum_page", "fail")
                msg.display(ut.time_str("time"), "load failed: NO." + str(stats.success_sum_page + 1) + " sum page (phantomjs)", "error")
                msg.log(self.task_name, ut.time_str("full"), "fail sum page: NO." + str(stats.success_sum_page + 1) + " (phantomjs)", "error")
                break

        if self.sum_page_number > 1:
            browser.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS

    def crawl_run(self):
        self.crawl_direct()  # 先爬第一sum-page
        self.crawl_phantom()  # 爬剩下的所有页


if __name__ == '__main__':
    spider_test = Spider_pm("test run","cancer", "liver,cancer", 100)
    spider_test.crawl_run()