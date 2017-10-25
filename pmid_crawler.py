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

import agents
import mongodb_handler as mh
import journal as jn
import utilities as ut
import message as msg
import stats
import config

existed_pmid_set = []

def save_png(browser):
    browser.save_screenshot(ut.cur_file_dir() + "/browser/" + ut.time_str("time") + ".png" )
    msg.msg("screenshot", "", "saved", "succ", "debug", msg.display, msg.log)


def parse_url(project, sstr): # 把keyword变成链接形式，临时这样，未来增加内容
    sstr_type = mh.read_sstr_type(project, sstr)
    if sstr_type == "key_words":
        if "," in sstr:
            sstr = sstr.replace(", ",",") # 防止有空格
            sstr = sstr.replace(",","%2C") # 换成链接形式
        else:
            pass
    if sstr_type == "expression":
        pass
    url = "https://www.ncbi.nlm.nih.gov/pubmed/?term=" + sstr  # 最初的查询网址
    msg.msg("url", "", "", url, "debug", msg.log, msg.display)
    return url


def adjust_record_number(project, sstr, record_number): # 确定正确的记录数
    url = parse_url(project, sstr)
    tries = config.request_sp_tries # 尝试3次
    while(tries > 0):
        try:
            opener = requests.Session()
            content = opener.get(url, timeout=config.request_time_out, headers=agents.get_header()).text # header仍然可以是随机的              
            max_record_number_start = content.find("<h3 class=\"result_count left\">Items:") + 37 # 找描述开始地方
            max_record_number_end = content.find('</h3>', max_record_number_start)
            record_number_str = content[max_record_number_start:max_record_number_end]
            max_record_number = int(record_number_str.split(" ")[-1])
            if max_record_number >= record_number:
                pass
            else:
                record_number = max_record_number
                msg.msg("record number", "", "changed", str(record_number),"notice", msg.log, msg.display)
            return record_number
            break
        except Exception, e:
            msg.msg("record number", "", "read", str(e), "error", msg.log)
            msg.msg("record number", "", "read", "retried", "notice", msg.display)
            tries -= 1
            time.sleep(config.request_refresh_wait)   
    else:
        msg.msg("record number", "", "read", "fail", "error", msg.display, msg.log)


def extract_new_pmid(content): # 从文本中提取pmid的通用办法
    pmid_set = []
    pmid_raw = re.findall("<dd>\d{8}</dd>", content)
    for pmid in pmid_raw:
        pmid = str(pmid[4:-5]) # 去处括号
        msg.msg("pmid", str(pmid), "retrieved", "proc", "info", msg.log, msg.display, msg.stat)
        if pmid not in existed_pmid_set:
            pmid_set.append(pmid)
            msg.msg("pmid", str(pmid), "retrieved", "succ", "info", msg.log, msg.display, msg.stat)
        else:
            msg.msg("pmid", str(pmid), "skipped", "skip", "info", msg.log, msg.display, msg.stat)
    return pmid_set


def crawl_direct(project, sstr):  # 用于直接爬sum-page，只能爬第一页，但是不采用phantomjs，速度快
    url = parse_url(project, sstr)
    tries = config.request_sp_tries # 尝试3次
    while(tries > 0):
        try:
            opener = requests.Session()
            content = opener.get(url, timeout=config.request_time_out, headers=agents.get_header()).text # header仍然可以是随机的              
            msg.msg("sum page", "1", "loaded", "proc", "info", msg.display, msg.log)
            pmid_list = extract_new_pmid(content) # 提取pmid, 然后排除旧的
            if pmid_list:
                mh.add_new_pmid_all(project, sstr, ut.time_str("full"), "pm", pmid_list)
            msg.msg("sum page", "1", "loaded", "succ", "info", msg.display, msg.log)
            break
        except Exception, e:
            msg.msg("sum page", "1", "loaded", str(e), "error", msg.log)
            msg.msg("sum page", "1", "loaded", "retried", "notice", msg.display)
            tries -= 1
            time.sleep(config.request_refresh_wait)   
    else:
        msg.msg("sum page", "1", "loaded", "fail", "error", msg.log, msg.display)
        

def crawl_phantom(project, sstr, record_number):  # 用于使用phantomjs爬取sum-page，可以爬无限页，但是速度慢
    url = parse_url(project, sstr)
    
    sum_page_number = int(math.ceil(record_number / 200)) # 计算要多少页面可以爬完
    rest_page_number = sum_page_number # 剩下多少页, 刚开始一样的
    
    tries_1st_sp = config.phantom_1st_sp_tries

    phantomjs_headers = agents.get_header() # 随机选择一个以供浏览器使用
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = (phantomjs_headers)  # header每次打开phantomjs是随机的，但浏览器关闭前不会变
    dcap["phantomjs.page.settings.loadImages"] = False  # 不载入图片，以加快速度
    # browser = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe', desired_capabilities=dcap)  # 加载浏览器，windows下使用
    path = ut.cur_file_dir() + "/browser/phantomjs" # 浏览器地址
    browser = webdriver.PhantomJS(executable_path=path, desired_capabilities=dcap)  # 加载浏览器
    browser.set_page_load_timeout(config.phantom_time_out)  # 设定网页加载超时,超过了就不加载
    while (tries_1st_sp > 0):
        try:
            browser.get(url) # 打开链接
            msg.msg("sum page", "1", "loaded", "proc", "info", msg.log, msg.display, msg.stat)
            WebDriverWait(browser, config.phantom_time_out).until(EC.presence_of_element_located((By.ID, "footer"))) # 等待加载完毕的最好方案
            browser.find_elements_by_name("Display")[2].click() # 找到下拉菜单，点击
            browser.implicitly_wait(1) # 等0.5秒钟，让菜单下拉完成               
            browser.find_element_by_xpath("//*[@id=\"ps200\"]").click() # 下拉菜单找到200这个值，点击
            WebDriverWait(browser, config.phantom_time_out).until(EC.presence_of_element_located((By.ID, "footer"))) # 自动刷新页面, 等待刷新完毕
            msg.msg("sum page", "1", "display number", "clicked", "debug", msg.display, msg.log)
            pmid_list = extract_new_pmid(browser.page_source)
            if pmid_list:
                mh.add_new_pmid_all(project, sstr, ut.time_str("full"), "pm", pmid_list) # 把pmid存起来
            msg.msg("sum page", "1", "loaded", "succ", "info", msg.log, msg.display, msg.stat)
            rest_page_number -= 1
            break
        except Exception as e:
            tries_1st_sp -= 1
            browser.refresh()
            browser.implicitly_wait(config.phantom_refresh_wait)
            msg.msg("sum page", "1", "loaded", "retried", "notice", msg.display)
            msg.msg("sum page", "1", "loaded", str(e), "error", msg.log)
    else:
        msg.msg("sum page", "1", "loaded", "failed", "error", msg.log, msg.display)
    while(rest_page_number > 0 and tries_1st_sp > 0):  # 确认需要第二页，如果sum-page只有1页，那就不用再打开; 如果第一页打开失败，也不用打开；从这里开始循环，直到所有的页面都爬完为止
        tries_other_sp = config.phantom_other_sp_tries
        while(tries_other_sp > 0):  # 尝试多少次，默认尝试3次，不行就打不开
            try:
                browser.find_element_by_link_text("Next >").click()  # 直接就点开“下一页”，从第二页开始
                WebDriverWait(browser, config.phantom_time_out).until(EC.presence_of_element_located((By.ID, "footer")))
                msg.msg("sum page", str(stats.processed_sum_page + 1), "loaded", "proc", "info", msg.log, msg.display, msg.stat)
                pmid_list = extract_new_pmid(browser.page_source)
                if pmid_list: # 防止空（所有pmid都被跳过了）
                    mh.add_new_pmid_all(project, sstr, ut.time_str("full"), "pm", pmid_list)
                msg.msg("sum page", str(stats.processed_sum_page + 1), "loaded", "succ", "info", msg.log, msg.display, msg.stat) 
                rest_page_number -= 1
                break
            except Exception as e:
                tries_other_sp -= 1                   
                browser.refresh()
                browser.implicitly_wait(config.phantom_refresh_wait)
                msg.msg("sum page", str(stats.processed_sum_page + 1), "loaded", "retried", "notice", msg.display)
                msg.msg("sum page", str(stats.processed_sum_page + 1), "loaded", str(e), "error", msg.log)
        else:
            msg.msg("sum page", str(stats.processed_sum_page + 1), "loaded", "failed", "error", msg.log, msg.display)
            break
    browser.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS


def crawl_run(project, sstr, record_number):
    global existed_pmid_set
    msg.msg("task", "", "started", "", "important", msg.display, msg.log)
    existed_pmid_set = mh.read_pmid_all(project) # 只读一次
    record_number = adjust_record_number(project, sstr, record_number) # 看看有没有那么多record
    if record_number <= 20:   
        crawl_direct(project, sstr) # 目标条数小于20时，直接爬
    else:
        crawl_phantom(project, sstr, record_number) # 目标条数大于20时，用phantomjs爬
    msg.msg("task", "", "finished", "", "important", msg.display, msg.log)


if __name__ == '__main__':
    crawl_run("cancer", "lung,cancer", 2000)