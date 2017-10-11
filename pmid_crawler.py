# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name: pmid_crawler.py
   Description: 蜘蛛类，只爬pubmed的pmid；实验新想法
   Author: Dexter Chen
   Date：2018-10-10
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

import agents
import mongodb_handler as mh
import journal as jn
import utilities as ut
import message as msg
import stats

# key_words = key_words  # 输入关键词，关键词是一个集合
# record_number = record_number  # 需要爬多少个
# project_name = project_name  # 项目的名字
# task_name = task_name

request_time_out = 30 # request超时时间
phantomjs_time_out = 60 # phantom超时时间
request_refresh_wait = 3 # request刷新等待
phantomjs_refresh_wait = 5 # 浏览器刷新等待

tries_request = 3
tries_1st_sp = 3  # 尝试获取第一个页面的次数
tries_other_sp = 5  # 尝试获取其它每个页面的次数

# sum_page_number = int(math.ceil(record_number / 20))  # 每页20个，计算共多少页
url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + "breast+cancer"  # 最初的查询网址

phantomjs_headers = agents.get_header() # 随机选择一个以供浏览器使用
pmid_set = mh.read_pmid_all() # 只读一次


def crawl_direct():  # 用于直接爬sum-page，只能爬第一页，但是不采用phantomjs，速度快
    tries = 3 # 尝试3次
    pmid_set = []
    while(tries > 0):
        try:
            opener = requests.Session()
            raw = opener.get(url, timeout=request_time_out, headers=agents.get_header()).text # header仍然可以是随机的              
            # soup = BeautifulSoup(raw)
            pmid_set_raw = re.findall("<dd>\\d*?</dd>", raw)
            for pmid in pmid_set_raw:
                pmid_set.append(pmid[4:-5])
            break
        except Exception, e:
            print e
            tries -= 1
            time.sleep(request_refresh_wait)   
    else:
        print "error"
    return pmid_set
        

def crawl_phantom(sum_page_number):  # 用于使用phantomjs爬取sum-page，可以爬无限页，但是速度慢
    rest_page_number = 3 # 剩下多少页
    tries_1st_sp = 3
    tries_other_sp = 3
    
    if sum_page_number > 1: # 如果页面不超过1个，就不启动浏览器
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
        dcap["phantomjs.page.settings.userAgent"] = (phantomjs_headers)  # header每次打开phantomjs是随机的，但浏览器关闭前不会变
        dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
        # browser = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器，windows下使用
        path = ut.cur_file_dir() + "/browser/phantomjs" # 浏览器地址
        browser = webdriver.PhantomJS(executable_path=path, desired_capabilities=dcap)  # 加载浏览器
        browser.set_page_load_timeout(phantomjs_time_out)  # 设定网页加载超时,超过了就不加载
    while (sum_page_number > 1 and tries_1st_sp > 0):
        try:
            browser.get(url)
            WebDriverWait(browser, phantomjs_time_out).until(EC.presence_of_element_located((By.ID, "footer")))
            browser.find_elements_by_name("Display")[2].click()
            browser.implicitly_wait(1)
            browser.save_screenshot(ut.cur_file_dir() + "/browser/" + ut.time_str("time") + ".png" )
            browser.find_element_by_xpath("//*[@id=\"ps200\"]").click()
            WebDriverWait(browser, phantomjs_time_out).until(EC.presence_of_element_located((By.ID, "footer")))
            browser.save_screenshot(ut.cur_file_dir() + "/browser/" + ut.time_str("time") + ".png" )

            print "successful"
            browser.quit()
            break

        except Exception as e:
            tries_1st_sp -= 1
            browser.refresh()
            browser.implicitly_wait(phantomjs_refresh_wait)
            print e
            print "refreshing"
    else:
        print "error"


#     while(rest_page_number > 1 and tries_1st_sp > 0):  # 确认需要第二页，如果sum-page只有1页，那就不用再打开; 如果第一页打开失败，也不用打开；从这里开始循环，直到所有的页面都爬完为止
#         msg.stat("sum_page", "proc")
#         tries_other_sp = self.tries_other_sp
        
#         while(tries_other_sp > 0):  # 尝试多少次，默认尝试5次，不行就打不开
#             try:
#                 browser.find_element_by_link_text("Next >").click()  # 直接就点开“下一页”，从第二页开始
#                 WebDriverWait(browser, self.phantomjs_time_out).until(EC.presence_of_element_located((By.ID, "footer")))
                
#                 msg.display(ut.time_str("time"), "loaded: NO." + str(stats.success_sum_page + 1) + " sum page (phantomjs)", "info")   
#                 msg.log(self.task_name, ut.time_str("full"), "load sum page: NO." + str(stats.success_sum_page + 1) + " (phantomjs)", "info")
                                    
#                 soup = BeautifulSoup(browser.page_source)
#                 self.author = soup.findAll(name='p', attrs={"class": "desc"})
#                 self.journal = soup.findAll(name="span", attrs={'class': 'jrnl'})
#                 self.title = soup.findAll(name='p', attrs={"class": "title"})
#                 self.issue = soup.findAll(name="p", attrs={'class': 'details'})
#                 self.pmid = soup.findAll(name="dd")
#                 self.generate_record()  # 直接产生结果

#                 msg.stat("sum_page", "succ")
#                 rest_page_number -= 1
#                 break
            
#             except Exception as e:
#                 tries_other_sp -= 1
#                 msg.display(ut.time_str("time"), "load retrying: NO." + str(stats.success_sum_page + 1) + " sum page (phantomjs); " + str(tries_other_sp) + " tries left", "notice")
#                 msg.log(self.task_name, ut.time_str("full"), "retry sum page: NO." + str(stats.success_sum_page + 1) + " (phantomjs)", "notice")
#                 msg.log(self.task_name, ut.time_str("full"), str(e), "error")
                
#                 browser.refresh()
#                 browser.implicitly_wait(self.phantomjs_refresh_wait)

#         else:
#             msg.stat("sum_page", "fail")
#             msg.display(ut.time_str("time"), "load failed: NO." + str(stats.success_sum_page + 1) + " sum page (phantomjs)", "error")
#             msg.log(self.task_name, ut.time_str("full"), "fail sum page: NO." + str(stats.success_sum_page + 1) + " (phantomjs)", "error")
#             break

#     if self.sum_page_number > 1:
#         browser.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS

# def crawl_run(self):
#     self.crawl_direct()  # 先爬第一sum-page
#     self.crawl_phantom()  # 爬剩下的所有页



if __name__ == '__main__':
    print crawl_phantom(2)